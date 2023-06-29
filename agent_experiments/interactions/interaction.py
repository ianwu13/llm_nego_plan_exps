"""
Base class for all interactions ("InteractionManager")
"""

import sys
import copy

from interaction_utils.interaction_logger import InteractionLogger


class InteractionManager(object):
    """Base handler for every model."""

    def __init__(self, dialog, ctx_file, logger=None, **kwargs):
        self.dialog = dialog
        self.logger = logger if logger else InteractionLogger()
        
        self.create_ctxs(ctx_file)

    # Utils for interaction setting (context)
    def create_ctxs(ctx_file):
        self.ctxs = []
        with open(ctx_file, 'r') as f:
            ctx_pair = []
            for line in f:
                ctx = line.strip().split()
                ctx_pair.append(ctx)
                if len(ctx_pair) == 2:
                    self.ctxs.append(ctx_pair)
                    ctx_pair = []

    def iter_ctx():
        for e in range(nepoch):
            random.shuffle(self.ctxs)
            for ctx in self.ctxs:
                yield ctx

    def sample_ctx():
        return random.choice(self.ctxs)

    # Run an interaction
    def run(self):
        print('Not Implemented in parent class "InteractionManager"')
        pass
