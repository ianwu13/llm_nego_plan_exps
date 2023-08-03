import json

DND_ITEMS = ['books', 'hats', 'balls']
DND_LABELS = [
    'greet',
    'inquire',
    'propose',
    'disagree',
    'insist',
    'agree',
    'unknown',
    '<selection>'
]

CASINO_ITEMS = ['food', 'water', 'firewood']
CUST_LABELS = [
    'smalltalk',
    'empathy coordination',
    'no need',
    'elicit preference',
    'undervalue',
    'vouch fairness',
    'express preference',
    'propose',
    'disagree',
    'agree',
    'unknown',
    '<selection>'
]


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever


def check_typo(path, labels, items):
    for d in json.load(open(path, 'r')):
        for u in d:
            if isinstance(u[1], str):
                u[1] = [u[1]]

            for lab in u[1]:
                valid = False
                slots = False
                for l in labels:
                    if lab.startswith(l):
                        valid = True
                        if lab != l:
                            slots = True
                            slots_str = remove_prefix(lab, l)
                        break

                if not valid:
                    print(lab)
                    continue
            
                if slots:
                    for i in [i.split('=')[0] for i in slots_str.split()]:
                        if i not in items:
                            print(lab)
                            break


def main():
    print('\nDND\n')
    check_typo('dnd_valset.json', DND_LABELS, DND_ITEMS)

    print('\nCaSiNo - DND\n')
    check_typo('casino_dndform_valset.json', DND_LABELS, CASINO_ITEMS)

    print('\nCaSiNo - Custom\n')
    check_typo('casino_customform_valset.json', CUST_LABELS, CASINO_ITEMS)


if __name__ == '__main__':
    main()
