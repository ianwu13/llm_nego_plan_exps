from collections import defaultdict


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


def parse_acts(da_toks: list, labels: list, items: list) -> list:
    # returns a list of dialogue acts
    # for example, 
    #       parse_acts("greet inquire firewood propose water=3")
    #             --> ["greet", "inquire firewood", "propose water=3"]
    if da_toks[-1] == '<eos>':
        da_toks = da_toks[:-1]
    splt_toks = da_toks
    if splt_toks[0] in ['YOU:', 'THEM:']:
        splt_toks.pop(0)

    # Get labels
    slots_dict = defaultdict(lambda: [False])
    annot_iter = hack_iter(splt_toks)

    cur = next(annot_iter)
    while cur:
        if cur in labels:
            slots_dict[cur][0] = True

            tmp_cur = cur
            cur, slots = slot_getter(annot_iter, labels, items)
            slots_dict[tmp_cur].extend(slots)
        elif cur == '<selection>':
            return [('<selection>')]
        else:
            print(f'Invalid annot found: {cur}. Full utterance annots: "{u}"')
            cur = next(annot_iter)
    
    # If label has been found but does not have necessary slots, remove
    if len(slots_dict['propose']) < 2:
        slots_dict.pop('propose')
    # Make sure there are still some labels or set to unknown
    has_labels = False
    for l in slots_dict:
        if l[0]:
            has_labels = True
            break
    if not has_labels:
        return [('unknown')]
        
    return [(k, v[1:]) for k, v in slots_dict.items()]


def seperate_slots_w_values(slots_list: list):
    s_vals, s_no_vals = [], []
    for s in slots_list:
        if '=' in s:
            s_splt = s.split('=')
            s_vals.append(f'{s_splt[1]} {s_splt[0]}')
        else:
            s_no_vals.append(s)
        
    return s_vals, s_no_vals