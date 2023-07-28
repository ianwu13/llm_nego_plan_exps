from agents.base_agent import Agent

from simple_utils import remove_prefix


class SingleLevelAgent(Agent):
    """An agent that uses DialogModel as an AI."""
    def __init__(self, model, rpf, cpf, args=None, name='AI'):
        super(SingleLevelAgent, self).__init__()
        self.model = model
        self.rpf = rpf  # "Response prompt function"
        self.cpf = cpf  # "Choice prompt function"
        self.name = name
        self.human = False

    def feed_context(self, ctx):
        # Reset/track dialogue contents
        self.dialogue = []

        self.ctx = ctx

    def write(self):
        # generate a new utterance
        response_prompt = self.rpf({
            'ctx': self.ctx,
            'dialogue': self.dialogue
        })
        response = self.model.get_model_outputs(response_prompt)[0]
        response_sp = response.split()

        if response_sp[0] != 'YOU:':
            # first add the special 'YOU:' token if necessary
            self.dialogue.append('YOU:')
        else:
            # Remove you token from response string if necessary
            response = remove_prefix(response, 'YOU:').lstrip()
        # then append the utterance
        self.dialogue.extend(response_sp)

        return response.split()

    def read(self, inpt):
        # first add the special 'YOU:' token if necessary
        self.dialogue.append('THEM:')
        # then append the utterance
        self.dialogue.extend(inpt)

    def choose(self):
        # generate a new utterance
        choice_prompt = self.cpf({
            'ctx': self.ctx,
            'dialogue': self.dialogue
        })
        choice_vals = self.model.get_model_outputs(choice_prompt)[0]

        try:
            choice_vals = [int(c) for c in choice_vals.split()]
            # Choice format: "['item0=1', 'item1=0', 'item2=3', 'item0=0', 'item1=1', 'item2=0']"
            choice = ['', '', '', '', '', '']
            if len(choice_vals) == 3:
                for i in range(3):
                    choice[i] = f'item{i}={choice_vals[i]}'
                    avail = int(self.ctx[i*2])
                    assert choice_vals[i] <= avail
                    choice[i+3] = f'item{i}={avail - choice_vals[i]}'
            elif len(choice_vals) == 6:
                for i in range(3):
                    choice[i] = f'item{i}={choice_vals[i]}'
                    choice[i+3] = f'item{i}={choice_vals[i+3]}'
            else:
                raise Exception('Length of choice output from model must be length 3 or 6')

            return choice
        except Exception as e:
            print(f'Choice values could not be parsed from model response: "{choice_vals}", self.ctx: {self.ctx}')
            print(e)
            return ['<no_agreement>' for _ in range(3)]

