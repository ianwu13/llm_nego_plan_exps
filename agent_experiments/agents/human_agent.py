import sys

from agents.base_agent import Agent
from data.word_corpus import STOP_TOKENS


class HumanAgent(Agent):
    """An agent that is used by a human to converse with AI."""
    def __init__(self, name='Human'):
        self.name = name
        self.human = True

    def feed_context(self, ctx):
        self.ctx = ctx

    def write(self):
        while True:
            try:
                inpt = input('%s : ' % self.name).lower().strip().split()
                if inpt[-1] in STOP_TOKENS:
                    return inpt
                return inpt + ['<eos>']
            except KeyboardInterrupt:
                sys.exit()
            except:
                print('Your sentence is invalid! Try again.')

    def parse_human_choice(self, inpt, output):
        cnts = [int(n) for n in inpt[0::2]]
        choice = [int(x) for x in output.strip().split()]

        if len(choice) != len(cnts):
            raise Exception(f'Invalid seleciton length; Choice len: {len(choice)}, Cnts len: {len(cnts)}')
        for x, n in zip(choice, cnts):
            if x < 0 or x > n:
                raise Exception(f'Invalid selection value, Choice={x}, N_available={n}')
        return [f'item{i}={x}' for i, x in enumerate(choice)]

    def choose(self):
        while True:
            try:
                choice = input('%s choice: ' % self.name)
                return self.parse_human_choice(self.ctx, choice)
            except KeyboardInterrupt:
                sys.exit()
            #except:
            #    print('Your choice is invalid! Try again.')
