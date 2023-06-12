from interactions.interaction import InteractionManager, InteractionLogger


class BotBotSelfPlay(InteractionManager):
    """Selfplay runner."""
    def __init__(self, dialog, ctx_file, logger=None, **kwargs):
        super(BotBotSelfPlay, self).__init__(dialog, ctx_file, logger, **kwargs)
        
        # MAY BE NECESSARY TO PASS COMMAND LINE ARGS LATER
        # self.args = args

    def run(self):
        n = 0
        # goes through the list of contexes and kicks off a dialogue
        for ctxs in self.iter_ctx():
            n += 1
            self.logger.dump('=' * 80)

            self.dialog.run(ctxs, self.logger)

            self.logger.dump('=' * 80)
            self.logger.dump('')

            if n % 100 == 0:
                self.logger.dump(f'{n}: {self.dialog.show_metrics()}', forced=True)
