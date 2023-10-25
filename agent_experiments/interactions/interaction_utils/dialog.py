# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
import logging
import numpy as np

from interactions.interaction_utils.metrics import MetricsContainer


class Dialog(object):
    """Dialogue runner."""
    def __init__(self, agents, args, scale_rw = 1.0, selection_length=6, rw_type="own_points", conf=None):
        # for now we only suppport dialog of 2 agents
        assert len(agents) == 2
        self.agents = agents
        self.args = args
        self.scale_rw = scale_rw
        self.selection_length = selection_length
        self.rw_type = rw_type
        self.conf = conf

        if args.max_turns:
            self.max_utts = args.max_turns
        else:
            self.max_utts = 20

        # Set up metric tracking
        self.metrics = MetricsContainer()
        self._register_metrics()

    def _read_lines(self, file_name):
        """Reads all the lines from the file."""
        assert os.path.exists(file_name), f'file does not exists {file_name}'
        lines = []
        with open(file_name, 'r') as f:
            for line in f:
                lines.append(line.strip())
        return lines

    def _register_metrics(self):
        """Registers valuable metrics."""
        self.metrics.register_average('dialog_len')
        self.metrics.register_average('sent_len')
        self.metrics.register_percentage('agree')
        self.metrics.register_average('advantage')
        self.metrics.register_time('time')
        self.metrics.register_average('comb_rew')
        for agent in self.agents:
            self.metrics.register_average(f'{agent.name}_rew')
            self.metrics.register_percentage(f'{agent.name}_sel')
            self.metrics.register_uniqueness(f'{agent.name}_unique')
        # text metrics
        ref_text = ' '.join(self._read_lines(self.args.ref_text))
        self.metrics.register_ngram('full_match', text=ref_text)

    def _is_selection(self, out):
        # return len(out) == 1 and out[0] == '<selection>'

        # Changed to looser criteria for selection
        utt = ''.join(out)
        return ('<selection>' in utt) or ('$selection#' in utt)

    def show_metrics(self):
        return ' '.join([f'\n\t{k}={v}' for k, v in self.metrics.dict().items()])

    # Taken from "ObjectDivisionDomain" class in end-to-end-negotiator repo
    def score_choices(self, choices, ctxs, rw_type="own_points", conf=None):
        """
        modified implementation:
            the conversation ends with a selection token or when max. number of utterances have been reached.
            if the conv. does not end in max turns - > 0 reward
            if the two outputs are numbers and exactly the same, -> positive reward
            if the two outputs are numbers and don’t match or one of them is no agreement - > they don’t match - > ignore this scenario = modeling failure.
            if the two outputs are no agreements and match -> 0 rewards.

        rw_type: type of the reward, as in config.rw_type
        conf: configuration in case the rw_type == "utility"
        """
        assert len(choices) == len(ctxs)

        if choices[0][0] == "<no_agreement>":
            for item in choices[0]:
                assert item == "<no_agreement>"

        if choices[1][0] == "<no_agreement>":
            for item in choices[1]:
                assert item == "<no_agreement>"
        
        if (choices[0][0] == "<no_agreement>" and choices[1][0] != "<no_agreement>") or (choices[1][0] == "<no_agreement>" and choices[0][0] != "<no_agreement>"):
            # failure mode; this case must simply be ignored.
            return -1, -1
        
        if (choices[0][0] == "<no_agreement>" and choices[1][0] == "<no_agreement>"):
            # both reach no agreement -> there is no agreement; give 0 rewards.
            agree, scores = False, [0 for _ in range(len(ctxs))]
            return agree, scores
        
        # at this point - both outputs are numbers only- if they match we give positive reward. if they don't, we ignore.            

        cnts = [int(x) for x in ctxs[0][0:6:2]]
        agree, scores = True, [0 for _ in range(len(ctxs))]
        for i, n in enumerate(cnts):
            for agent_id, (choice, ctx) in enumerate(zip(choices, ctxs)):
                try:
                    taken = int(choice[i][-1])
                except:
                    raise Exception('"choice[i][-1]" should be able to be converted to an int')
                n -= taken
                scores[agent_id] += int(ctx[2 * i + 1]) * taken
            agree = agree and (n == 0)
        
        if not agree:
            # this is again a failure mode - this just does not mean disagreement
            return -1, -1

        # no failures, positive outputs - same from both sides.
        if rw_type == "own_points":
            return agree, scores
        
        if rw_type == "partner_points":
            scores.reverse()
            return agree, scores

        if rw_type == "self_adv":
            scores = scores[:]
            rev_scores = scores[::-1]

            self_adv_scores = []
            for s, rs in zip(scores, rev_scores):
                adv = max([0.0, s - rs])
                self_adv_scores.append(adv)

            return agree, self_adv_scores
        
        if rw_type == "partner_adv":
            scores = scores[:]
            rev_scores = scores[::-1]

            partner_adv_scores = []
            for s, rs in zip(scores, rev_scores):
                adv = max([0.0, rs - s])
                partner_adv_scores.append(adv)

            return agree, partner_adv_scores
        
        if rw_type == "combine50_50":
            scores = scores[:]
            rev_scores = scores[::-1]

            # comb scores with equal weightage.
            equal_comb_scores = []
            for s, rs in zip(scores, rev_scores):
                comb = 0.5*s + 0.5*rs
                equal_comb_scores.append(comb)

            return agree, equal_comb_scores

        if rw_type == "combine75_25":
            scores = scores[:]
            rev_scores = scores[::-1]

            # comb scores inclined towards the self.
            self_comb_scores = []
            for s, rs in zip(scores, rev_scores):
                comb = 0.75*s + 0.25*rs
                self_comb_scores.append(comb)

            return agree, self_comb_scores
        
        if rw_type == "combine25_75":
            scores = scores[:]
            rev_scores = scores[::-1]

            # comb scores inclined towards the partner
            partner_comb_scores = []
            for s, rs in zip(scores, rev_scores):
                comb = 0.25*s + 0.75*rs
                partner_comb_scores.append(comb)

            return agree, partner_comb_scores
        
        if rw_type == "utility":
            # use the utility function
            assert conf
            scores = scores[:]
            rev_scores = scores[::-1]

            utility_scores = []
            for s, rs in zip(scores, rev_scores):
                comb = max([0, conf[0]*s + conf[1]*rs + conf[2]*max([0, rs - s]) + conf[3]*max([0, s - rs])])
                utility_scores.append(comb)

            return agree, utility_scores
        
        if rw_type == "fair":
            # use the utility function with a fixed fair objective
            
            scores = scores[:]
            rev_scores = scores[::-1]

            utility_scores = []
            for s, rs in zip(scores, rev_scores):
                comb = max([0, 1*s + 0*rs + (-0.75)*max([0, rs - s]) + (-0.75)*max([0, s - rs])])
                utility_scores.append(comb)

            return agree, utility_scores
        
        raise ValueError

    def run(self, ctxs, logger):
        """Runs one instance of the dialogue."""
        assert len(self.agents) == len(ctxs)

        #obj for storage
        storage = {
            "ctxs": {},
            "conv": [],
            "choices": {},
            "agreement_status": None,
            "rewards": {},
        }

        # initialize agents by feeding in the contexes
        for agent, ctx in zip(self.agents, ctxs):
            agent.feed_context(ctx)
            logger.dump_ctx(agent.name, ctx)
            storage["ctxs"][agent.name] = ctx
        logger.dump('-' * 80)

        # choose who goes first by random
        if np.random.rand() < 0.5:
            writer, reader = self.agents
        else:
            reader, writer = self.agents

        conv = []
        # reset metrics
        self.metrics.reset()

        curr = 0
        while curr < self.max_utts:
            # produce an utterance
            out = writer.write()

            self.metrics.record('sent_len', len(out))
            self.metrics.record('full_match', out)
            self.metrics.record('%s_unique' % writer.name, out)

            # append the utterance to the conversation
            conv.append(out)
            storage["conv"].append(
                {
                    "name": writer.name,
                    "sent": " ".join(out),
                }
            )
            # make the other agent to read it
            reader.read(out)
            if writer.human:
                logger.dump_human_sent(writer.name, out)
            else:
                logger.dump_sent(writer.name, out)
            # check if the end of the conversation was generated
            if self._is_selection(out):
                self.metrics.record('%s_sel' % writer.name, 1)
                self.metrics.record('%s_sel' % reader.name, 0)
                break
            writer, reader = reader, writer

            curr += 1

        choices = []
        if not self._is_selection(conv[-1]):
            # the conversation did not finish; assume disagreement.
            assert curr == self.max_utts, curr
            agree, rewards = False, [0 for _ in range(len(ctxs))]

            choices = [
                ["<no_agreement>", "<no_agreement>", "<no_agreement>"],
                ["<no_agreement>", "<no_agreement>", "<no_agreement>"],
            ]

            storage["agreement_status"] = "no_agreement_len"

            for agent, choice, in zip(self.agents, choices):
                storage["choices"][agent.name] = choice
        else:
            # the conversation atleast finished nicely; now we try to get a consistent output.
            # generate choices for each of the agents
            for agent in self.agents:
                choice = agent.choose()
                choices.append(choice)
                logger.dump_choice(agent.name, choice[: self.selection_length // 2])
                storage["choices"][agent.name] = choice[: self.selection_length // 2]

            # evaluate the choices, produce agreement and a reward
            agree, rewards = self.score_choices(choices, ctxs, rw_type=self.rw_type, conf=self.conf)
        
        if agree == -1 and rewards == -1:
            # this is neither an agreement, nor a disagreement - we don't know due to model failure.
            # print("Failure mode. - agree and rewards are both None. Ignoring this case.")
            print("Failure")

            storage["agreement_status"] = "mismatch_failure" # the choices of the two agents were different, hence, the output is inconclusive.
            return None, None, None, storage
        
        if not agree:
            # this is disagreement between the two.
            # print("Disagreement between the two models.")
            print("Disagreement")
            if not storage["agreement_status"]:
                # there is no agreement, which is not of type len.hence, it is of type wa.
                storage["agreement_status"] = "no_agreement_wa" #the choices match and end in a disagreement.
        else:
            # there is agreement
            storage["agreement_status"] = "agreement" # choices match and are numbers.
        
        for agent, reward in zip(self.agents, rewards):
            if storage["agreement_status"] == "agreement":
                storage["rewards"][agent.name] = reward
            elif "no_agreement" in storage["agreement_status"]:
                storage["rewards"][agent.name] = 0

        logger.dump('-' * 80)

        logger.dump_agreement(agree)
        # COMMENTED BECAUSE THIS REPO DOES NOT SUPPORT RL FOR AGENTS CURRENTLY
        # # perform update, in case if any of the agents is learnable
        for agent, reward in zip(self.agents, rewards):
            logger.dump_reward(agent.name, agree, reward)
        #     logging.debug("%s : %s : %s" % (str(agent.name), str(agree), str(rewards)))
        #     agent.update(agree, reward, scale_rw = self.scale_rw)

        if agree:
            self.metrics.record('advantage', rewards[0] - rewards[1])
        self.metrics.record('time')
        self.metrics.record('dialog_len', len(conv))
        self.metrics.record('agree', int(agree))
        self.metrics.record('comb_rew', np.sum(rewards) if agree else 0)
        for agent, reward in zip(self.agents, rewards):
            self.metrics.record('%s_rew' % agent.name, reward if agree else 0)

        logger.dump('-' * 80)
        logger.dump(self.show_metrics())
        logger.dump('-' * 80)
        for ctx, choice in zip(ctxs, choices):
            logger.dump('debug: %s %s' % (' '.join(ctx), ' '.join(choice)))

        return conv, agree, rewards, storage
