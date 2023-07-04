import random
import itertools

from interactions.interaction import InteractionManager
from interactions.interaction_utils import InteractionLogger


class BotHumanChat(InteractionManager):
    """A helper class that runs dialogues."""
    def __init__(self, dialog, ctx_file=None, logger=None, **kwargs):
        if ctx_file is not None:
            super(BotHumanChat, self).__init__(dialog, ctx_file, logger, **kwargs)
        else:
            self.dialog = dialog
            self.logger = logger if logger else InteractionLogger()

            self.auto_create_ctxs(**kwargs)

    def auto_create_ctxs(self, num_types=3, num_objects=10, max_score=10, **kwargs):
        self.num_types = num_types
        self.num_objects = num_objects
        self.max_value = max_value

    # Override to allowfor manual entry of context for a dialogue
    def iter_ctx(self):
        if self.ctxs is None:
            raise Exception(
                'Cannot call InteractionManager.iter_ctx() when a context file has not been provided. \
                Context examples should be obtained through InteractionManager.sample_ctx() in this case.'
                )

        for e in range(nepoch):
            random.shuffle(self.ctxs)
            for ctx in self.ctxs:
                yield ctx

    # Override to allowfor manual entry of context for a dialogue
    def sample_ctx(self):
        if self.ctxs is not None:
            return random.choice(self.ctxs)
        
        # Otherwise, get context manually
        while True:
            try:
                ctx1 = input('Input context: ')
                ctx1 = ctx1.strip().split()
                if len(ctx1) != 2 * self.num_types:
                    raise
                if np.sum([int(x) for x in ctx1[0::2]]) != self.num_objects:
                    raise
                if np.max([int(x) for x in ctx1[1::2]]) > self.max_value:
                    raise
                break
            except KeyboardInterrupt:
                sys.exit()
            except:
                print('The context is invalid! Try again.')
                print('Reason: num_types=%d, num_objects=%d, max_value=%s' % (
                    self.num_types, self.num_objects, self.max_value))
        # Get partner context
        ctx2 = copy.copy(ctx1)
        for i in range(1, len(ctx2), 2):
            ctx2[i] = np.random.randint(0, self.args.max_value + 1)
        return [ctx1, ctx2]

    def run(self):
        """Runs endless number of dialogues."""
        self.logger.dump('Running Bot-Human Chat')
        for dialog_id in itertools.count():
            self.logger.dump('=' * 80)
            self.logger.dump('Dialog %d' % dialog_id)
            self.logger.dump('-' * 80)

            ctxs = self.sample_ctx()
            self.dialog.run(ctxs, self.logger)

            self.logger.dump('=' * 80)
            self.logger.dump('')
