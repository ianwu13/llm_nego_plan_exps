"""
A class "InteractionLogger" for logging interaction outputs
"""

import sys


class InteractionLogger(object):
    """Logger for a dialogue."""
    CODE2ITEM = [
        ('item0', 'book'),
        ('item1', 'hat'),
        ('item2', 'ball'),
    ]
    CODE2ITEM_CASINO = [
        ('item0', 'firewood'),
        ('item1', 'water'),
        ('item2', 'food'),
    ]

    def __init__(self, dataset, verbose=False, log_file=None, append=False):
        self.logs = []  # List of locations to log to
        self.dataset = dataset
        if verbose:
            self.logs.append(sys.stderr)
        if log_file:
            flags = 'a' if append else 'w'
            self.log_file = open(log_file, flags)
            self.logs.append(self.log_file)

    def _dump(self, s, forced=False):
        for log in self.logs:
            print(s, file=log)
            log.flush()
        if forced:
            print(s, file=sys.stdout)
            sys.stdout.flush()

    def _dump_lf(self, s, forced=False):
        print(s, file=self.log_file)
        self.log_file.flush()
        if forced:
            print(s, file=sys.stdout)
            sys.stdout.flush()

    def dump(self, s, forced=False):
        self._dump(s, forced=forced)

    # Here down are wrappers to dump with special formatting
    def _dump_with_name(self, name, s):
        self._dump(f'{name:<5} : {s}')

    def dump_ctx(self, name, ctx):
        if self.dataset == "casino":
            index = ctx.index("=")
            value = ctx[0:index]
            reason = ctx[index + 1:]
            assert len(value) == 6, 'Expecting 3 objects'
            s = ' '.join(['%s=(count:%s value:%s)' % (self.CODE2ITEM_CASINO[i][1], value[2 * i], value[2 * i + 1]) \
                for i in range(3)])
            s = s + ' Preference: ' + ' '.join(reason) + '\n'
            self._dump_with_name(name, s)
      
        else:# dnd
            assert len(ctx) == 6, 'Expecting 3 objects'
            s = ' '.join(['%s=(count:%s value:%s)' % (self.CODE2ITEM[i][1], ctx[2 * i], ctx[2 * i + 1]) \
                for i in range(3)])
            self._dump_with_name(name, s)

    def dump_sent(self, name, sent):
        self._dump_with_name(name, ' '.join(sent))

    def dump_human_sent(self, name, sent):
        self._dump_lf(f'{name:<5} : {" ".join(sent)}')

    def dump_choice(self, name, choice):
        item_list = self.CODE2ITEM
        if self.dataset == 'casino':
            item_list = self.CODE2ITEM_CASINO
        
        def rep(w):
            p = w.split('=')
            if len(p) == 2:
                for k, v in item_list:
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
