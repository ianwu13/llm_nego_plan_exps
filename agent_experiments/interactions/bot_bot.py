from interactions.interaction import InteractionManager, InteractionLogger


class BotBotSelfPlay(InteractionManager):
    """Selfplay runner."""
    def __init__(self, dialog, dataset, ctx_file=None, logger=None, **kwargs):
        # super(BotBotSelfPlay, self).__init__(dialog, dataset, ctx_file, logger, **kwargs)
        if ctx_file is not None:
            super(BotBotSelfPlay, self).__init__(dialog, dataset, ctx_file, logger, **kwargs)
        else:
            self.dialog = dialog
            self.logger = logger if logger else InteractionLogger()

            self.auto_create_ctxs(**kwargs)
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
