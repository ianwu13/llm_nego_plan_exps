from collections import defaultdict

from fire import Fire


DND_ITEMS = ['books', 'hats', 'balls']
DND_LABELS = [
    'greet',
    'inquire',
    'propose',
    'disagree',
    'insist',
    'agree',
    'unknown',
]

CASINO_ITEMS = ['food', 'water', 'firewood']
CUST_LABELS = [
    'smalltalk',
    'empathycoordination',
    'noneed',  # NEED SLOTS
    'elicitpreference',
    'undervalue',  # NEED SLOTS
    'vouchfairness',
    'expresspreference',  # NEED SLOTS
    'propose',  # NEED SLOTS
    'disagree',
    'agree',
    'unknown',
]


def hack_iter(listy):
    for i in listy:
        yield i
    yield None


def slot_getter(annot_iterator, labels_list, items_list):
    slots_list = []
    
    cur = next(annot_iterator)
    while cur:
        valid = False
        for i in items_list:
            if cur.startswith(i) and not (cur.endswith('<slot>')) and ('>' not in cur) and ('<' not in cur):
                slots_list.append(cur)
                valid = True
                break
        if not valid:
            break

        cur = next(annot_iterator)
    
    # make set to remove duplicates
    slots_list = set(slots_list)
    
    # Sort slots order
    sorted_slots = []
    for i in items_list:
        for s in slots_list:
            if s.startswith(i):
                sorted_slots.append(s)

    return cur, sorted_slots


def main(in_file: str, out_file: str, dataset: str = 'dnd'):
    # Get proper labels
    if dataset == 'dnd':
        items = DND_ITEMS
        labels = DND_LABELS
    elif dataset == 'casino':
        items = CASINO_ITEMS
        labels = CUST_LABELS
        raise NotImplementedError(
            'This script is currently intended only for CaSiNo custom format cleaning. I have included dataset as an arg here to make room for future expansion if needed')
    else:
        raise Exception('dataset must be "dnd" or "casino"')

    lines = open(in_file, 'r').readlines()

    with open(out_file, 'w') as f:
        for line in lines:
            tmp = line.split(' <dialogue> ')
            prefix = ''.join([tmp[0],' <dialogue> '])
            tmp = tmp[1].split(' </dialogue> ')
            suffix = ''.join([' </dialogue> ', tmp[1]])
            dialogue = tmp[0]

            dia_splt = dialogue.split(' <eos> ')
            for i, u in enumerate(dia_splt):
                u_splt = u.split()
                assert u_splt[0] in ['YOU:', 'THEM:'], f'Splitting incorrect for this line: "{line}"'
                role = u_splt.pop(0)

                # Get labels
                slots_dict = defaultdict(lambda: [False])
                annot_iter = hack_iter(u_splt)

                cur = next(annot_iter)
                while cur:
                    if cur in labels:
                        slots_dict[cur][0] = True

                        tmp_cur = cur
                        cur, slots = slot_getter(annot_iter, labels, items)
                        slots_dict[tmp_cur].extend(slots)
                    elif cur == '<selection>':
                        slots_dict = False
                        break
                    else:
                        print(f'Invalid annot found: {cur}. Full utterance annots: "{u}"')
                        cur = next(annot_iter)

                if slots_dict:
                    # If label has been found but does not have necessary slots, remove
                    if len(slots_dict['propose']) < 2:
                        slots_dict['propose'][0] = False
                    # Make sure there are still some labels or set to unknown
                    has_slots = False
                    for l in slots_dict:
                        if l[0]:
                            has_slots = True
                            break
                    if not has_slots:
                        slots_dict['unknown'][0] = True

                    labels_list = [role]
                    for l in labels:
                        if slots_dict[l][0]:
                            labels_list.append(l)

                            sorted_slots = slots_dict[l][1:]
                            
                            # assert len(sorted_slots) <= 3, f'Too many slots for label {l}. Slots: {sorted_slots}\nUtterance:\n{u}'
                            # if not (len(sorted_slots) <= 3): print(f'Too many slots for label {l}. Slots: {sorted_slots}')

                            labels_list.extend(sorted_slots)
                else:
                    labels_list = [role, '<selection>']

                fixed_annots = ' '.join(labels_list)

                dia_splt[i] = fixed_annots

            # Construct dialgoue string
            dialogue = ' <eos> '.join(dia_splt)

            new_line = ''.join([prefix, dialogue, suffix])
            f.write(new_line)


if __name__ == '__main__':
    Fire(main)
    print('DONE')
