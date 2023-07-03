import torch

from agents.base_agent import Agent


class DualLevelAgent(Agent):
    def __init__(self, pg_model, p_prompt_func, g_prompt_func, planning_model, cpf, rpf=None, name='AI', temperature=1.0):
        super(DualLevelAgent, self).__init__()
        self.pg_model = pg_model  # parser/generator model
        self.p_prompt_func = p_prompt_func  # parser_prompt_func
        self.g_prompt_func = g_prompt_func  # generator_prompt_func
        self.planning_model = planning_model
        self.cpf = cpf  # "Choice prompt function"

        if self.planning_model.is_llm:
            assert rpf is not None
            self.rpf = rpf  # "Response prompt function"
        else:
            # Check that necessary gen methods exist if GRU is used
            assert hasattr(self.planning_model, 'context_dict'), 'planning_model must have "context_dict" attribute.'
            assert hasattr(self.planning_model, 'word_dict'), 'planning_model must have "word_dict" attribute.'
            assert hasattr(self.planning_model, 'forward_context'), 'planning_model must have "word_dict" method.'
            assert hasattr(self.planning_model, 'zero_hid'), 'planning_model must have "zero_hid" method.'
            assert hasattr(self.planning_model, 'read'), 'planning_model must have "read" method.'
            assert hasattr(self.planning_model, 'write'), 'planning_model must have "wrtie" method.'

            self.temperature = temperature

        self.name = name
        self.human = False

    def _encode(self, inpt, dictionary):
        """A helper function that encodes the passed in words using the dictionary.

        inpt: is a list of strings.
        dictionary: prebuild mapping, see Dictionary in data.py
        """
        encoded = torch.LongTensor(dictionary.w2i(inpt)).unsqueeze(1)
        
        if torch.cuda.is_available():
            if self.model.device_id is not None:
                encoded = encoded.cuda(self.model.device_id)
        return encoded

    def _decode(self, out, dictionary):
        """A helper function that decodes indeces into English words.

        out: variable that contains an encoded utterance.
        dictionary: prebuild mapping, see Dictionary in data.py
        """
        return dictionary.i2w(out.data.squeeze(1).cpu())

    def feed_context(self, context):
        # context - NL
        self.context = context
        # all the pronounced words - NL
        self.dialogue = []
        # all the dialogue acts - NL
        self.dialogue_acts = []

        if not self.planning_model.is_llm:
            # encoded context
            self.ctx = self._encode(context, self.planning_model.context_dict)
            # hidded state of context
            self.ctx_h = self.planning_model.forward_context(Variable(self.ctx))

            # the hidden state of all the dialogue acts
            self.da_hs = []

            # current hidden state of the dialogue acts rnn
            self.da_h = self.planning_model.zero_hid(1)

    def read(self, inpt):
        # Append to dialogue array
        self.dialogue.append('THEM:')
        self.dialogue.extend(inpt.split())

        # Get dialogue act with parser
        parser_prompt = self.p_prompt_func({
            'ctx': self.ctx,
            'dialogue': self.dialogue,
            'read_inpt': inpt
        })
        inpt_da = self.pg_model.get_model_outputs([parser_prompt])[0]  # Dialogue Act
        # And append to da array
        self.dialogue_acts.append('THEM:')
        self.dialogue_acts.extend(inpt_da.split())

        # Encode with GRU if necessary
        if not self.planning_model.is_llm:
            inpt = self._encode(inpt_da, self.planning_model.word_dict)
            da_hs, self.da_h = self.planning_model.read(Variable(inpt), self.da_h, self.ctx_h)
            # append new hidded states to the current list of the hidden states
            self.da_hs.append(da_hs.squeeze(1))

    def write(self):
        if not self.planning_model.is_llm:
            # generate a new utterance; 100 max words (third arg)
            _, outs, self.da_h, da_hs = self.planning_model.write(self.da_h, self.ctx_h, 100, self.temperature)
            # decode into English words
            resp_da = self._decode(outs, self.planning_model.word_dict)

            # Generate utterance response
            generator_prompt = self.g_prompt_func({
                'ctx': self.ctx,
                'dialogue': self.dialogue,
                'dia_acts': self.dialogue_acts,
                'gen_act': resp_da
            })
            write_utt = self.pg_model.get_model_outputs([generator_prompt])[0]  # Dialogue Act
            
            # append new hidded states to the current list of the hidden states
            self.da_hs.append(da_hs)
            # Store dialogue act response
            self.dialogue_acts.append('YOU:')
            self.dialogue_acts.extend(resp_da.split())
            # Store utterance response
            self.dialogue.append('YOU:')
            self.dialogue.extend(write_utt.split())

            return write_utt
        else:
            resp_da_prompt = self.rpf({
                'ctx': self.ctx,
                'dialogue': self.dialogue,
                'dia_acts': self.dialogue_acts
            })
            resp_da = self.pg_model.get_model_outputs([resp_da_prompt])[0]  # Dialogue Act

            # Generate utterance response
            generator_prompt = self.g_prompt_func({
                'ctx': self.ctx,
                'dialogue': self.dialogue,
                'dia_acts': self.dialogue_acts,
                'gen_act': resp_da
            })
            write_utt = self.pg_model.get_model_outputs([generator_prompt])[0]  # Dialogue Act
            
            # Store dialogue act response
            self.dialogue_acts.append('YOU:')
            self.dialogue_acts.extend(resp_da.split())
            # Store utterance response
            self.dialogue_acts.append('YOU:')
            self.dialogue_acts.extend(write_utt.split())

            return write_utt
    
    # SL Agent
    def choose(self):
        # generate a new utterance
        choice_prompt = self.cpf({
            'ctx': self.ctx,
            'dialogue': self.dialogue,
            'dia_acts': self.dialogue_acts
        })
        choice = self.model.get_model_outputs([response_prompt])[0]

        try:
            choice = [int(c) for c in choice.split()]
        except:
            print('Choice values could not be parsed from model response')
            return ['<no_agreement>' for _ in range(3)]

        return choice

    '''
    # Incomplete code to use GRU to make choice
    def choose(self):
        # get all the possible choices
        choices = self.domain.generate_choices(self.context)
        # concatenate the list of the hidden states into one tensor
        lang_hs = lang_hs if lang_hs is not None else torch.cat(self.lang_hs)
        # concatenate all the words into one tensor
        words = words if words is not None else torch.cat(self.dialogue)
        # logits for each of the item
        logits = self.model.generate_choice_logits(words, lang_hs, self.ctx_h)

        # construct probability distribution over only the valid choices
        choices_logits = []
        for i in range(self.domain.selection_length()):
            idxs = [self.model.item_dict.get_idx(c[i]) for c in choices]
            idxs = Variable(torch.from_numpy(np.array(idxs)))
            idxs = self.model.to_device(idxs)
            choices_logits.append(torch.gather(logits[i], 0, idxs).unsqueeze(1))

        choice_logit = torch.sum(torch.cat(choices_logits, 1), 1, keepdim=False)
        # subtract the max to softmax more stable
        choice_logit = choice_logit.sub(choice_logit.max().item())

        # http://pytorch.apachecn.org/en/0.3.0/_modules/torch/nn/functional.html
        # choice_logit.dim() == 1, so implicitly _get_softmax_dim returns 0
        prob = F.softmax(choice_logit,dim=0)
        if sample:
            # sample a choice
            idx = prob.multinomial().detach()
            logprob = F.log_softmax(choice_logit).gather(0, idx)
        else:
            # take the most probably choice
            _, idx = prob.max(0, keepdim=True)
            logprob = None

        return choices[idx.item()][:self.domain.selection_length()]
    '''