"""
Base class for all interactions ("InteractionManager")
    A class ("InteractionLogger") for logging interaction outputs is also included
"""

import sys
import copy


class InteractionLogger(object):
    """Logger for a dialogue."""
    CODE2ITEM = [
        ('item0', 'book'),
        ('item1', 'hat'),
        ('item2', 'ball'),
    ]

    def __init__(self, verbose=False, log_file=None, append=False):
        self.logs = []  # List of locations to log to
        if verbose:
            self.logs.append(sys.stderr)
        if log_file:
            flags = 'a' if append else 'w'
            self.logs.append(open(log_file, flags))

    def _dump(self, s, forced=False):
        for log in self.logs:
            print(s, file=log)
            log.flush()
        if forced:
            print(s, file=sys.stdout)
            sys.stdout.flush()

    def dump(self, s, forced=False):
        self._dump(s, forced=forced)

    # Here down are wrappers to dump with special formatting
    def _dump_with_name(self, name, s):
        self._dump(f'{name:<5} : {s}')

    def dump_ctx(self, name, ctx):
        assert len(ctx) == 6, 'Expecting 3 objects'
        s = ' '.join(['%s=(count:%s value:%s)' % (self.CODE2ITEM[i][1], ctx[2 * i], ctx[2 * i + 1]) \
            for i in range(3)])
        self._dump_with_name(name, s)

    def dump_sent(self, name, sent):
        self._dump_with_name(name, ' '.join(sent))

    def dump_choice(self, name, choice):
        def rep(w):
            p = w.split('=')
            if len(p) == 2:
                for k, v in self.CODE2ITEM:
                    if p[0] == k:
                        return '%s=%s' % (v, p[1])
            return w

        self._dump_with_name(name, ' '.join([rep(c) for c in choice]))

    def dump_agreement(self, agree):
        self._dump('Agreement!' if agree else 'Disagreement?!')

    def dump_reward(self, name, agree, reward):
        if agree:
            self._dump_with_name(name, '%d points' % reward)
        else:
            self._dump_with_name(name, '0 (potential %d)' % reward)


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
