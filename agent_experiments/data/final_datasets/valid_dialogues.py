from fire import Fire


def line_valid(line: str):
    tmp = line.split(' <dialogue> ')[1].split(' </dialogue> ')
    dialogue = tmp[0]
    utterances = [u.split() for u in dialogue.split(' <eos> ')]
    if tmp[1].split(' </output> ')[0] == '<output> <no_agreement> <no_agreement> <no_agreement> <no_agreement> <no_agreement> <no_agreement>':
        return True
    final_deal = [int(i.split('=')[1])
                  for i in tmp[1].split(' </output> ')[0].split()[1:]]

    proposals = {
        'YOU:': [],
        'THEM:': []
    }
    for i, item in enumerate(['food', 'water', 'firewood']):
        for u in reversed(utterances):
            found = False
            for j, tok in enumerate(u[1:]):
                if tok == 'propose':
                    # Get all the slots for just propose label
                    slots = u[j+2:j+5]
                    slots_len = 0
                    for s in slots:
                        val_slot = False
                        for pref in ['food', 'water', 'firewood']:
                            if s.startswith(pref):
                                val_slot = True
                                slots_len += 1
                                break
                        if not val_slot:
                            break
                    slots = slots[:slots_len]

                    # Check if theres a slot for "item" and if so recrd the numbers
                    for s in slots:
                        if s.startswith(item):
                            utterer = u[0]
                            partner = 'THEM:' if utterer == 'YOU:' else 'YOU:'
                            try:
                                utterer_gets = int(s.split('=')[1])
                            except:
                                print(s)
                                exit()
                            partner_gets = 3 - utterer_gets

                            proposals[utterer].append(utterer_gets)
                            proposals[partner].append(partner_gets)

                            found = True
                            break
                if found:
                    break
            if found:
                break
        if not found:
            # Item is never even proposed in all utterances
            return False

    prop_deal = proposals['YOU:'] + proposals['THEM:']

    return prop_deal == final_deal


def fix_line(line: str):
    tmp = line.split(' <dialogue> ')
    prefix = tmp[0] + ' <dialogue> '
    tmp = tmp[1].split(' </dialogue> ')
    suffix = ' </dialogue> ' + tmp[1]
    dialogue = tmp[0]
    utterances = [u.split() for u in dialogue.split(' <eos> ')]
    final_deal = [int(i.split('=')[1])
                  for i in tmp[1].split(' </output> ')[0].split()[1:]]

    proposals = {
        'YOU:': [],
        'THEM:': []
    }
    for i, item in enumerate(['food', 'water', 'firewood']):
        for k, u in enumerate(reversed(utterances)):
            u_ind = -(k+1)
            found = False
            for j, tok in enumerate(u[1:]):
                if tok == 'propose':
                    # Get all the slots for just propose label
                    slots = u[j+2:j+5]
                    slots_len = 0
                    for s in slots:
                        val_slot = False
                        for pref in ['food', 'water', 'firewood']:
                            if s.startswith(pref):
                                val_slot = True
                                slots_len += 1
                                break
                        if not val_slot:
                            break
                    slots = slots[:slots_len]

                    # Check if theres a slot for "item" and if so recrd the numbers
                    for s in slots:
                        if s.startswith(item):
                            utterer = u[0]
                            partner = 'THEM:' if utterer == 'YOU:' else 'YOU:'
                            try:
                                utterer_gets = int(s.split('=')[1])
                            except:
                                print(s)
                                exit()
                            partner_gets = 3 - utterer_gets

                            proposals[utterer].append(utterer_gets)
                            proposals[partner].append(partner_gets)

                            prop_ind = u.index('propose')
                            if u[prop_ind:].count(s) != 1:
                                return False, ''
                            slot_ind = u[prop_ind:].index(s) + prop_ind
                            true_count = final_deal[i] if utterer == 'YOU:' else final_deal[i+3]
                            utterances[u_ind][slot_ind] = f'{item}={true_count}'

                            found = True
                            break
                if found:
                    break
            if found:
                break
        if not found:
            # Item is never even proposed in all utterances
            return False, ''

    prop_deal = proposals['YOU:'] + proposals['THEM:']

    fixed_dialogue = ' <eos> '.join([' '.join(u) for u in utterances])
    fixed_line = ''.join([prefix, fixed_dialogue, suffix])
    return True, fixed_line


def fix_invalid(in_file: str, valid_out_file: str, invalid_out_file: str):
    valid_file = open(valid_out_file, 'w')
    invalid_file = open(invalid_out_file, 'w')

    valid_count = 0
    invalid_count = 0

    with open(in_file, 'r') as f:
        line = f.readline()
        while line:
            if line_valid(line):
                valid_file.write(line)
                valid_count += 1
            else:
                fixable, fixed_line = fix_line(line)
                if fixable:
                    valid_file.write(fixed_line)
                    valid_count += 1
                else:
                    invalid_file.write(line)
                    invalid_count += 1

            line = f.readline()

    print(f'Valid (fixable) Line Count: {valid_count}')
    print(f'Invalid (unfixable) Line Count: {invalid_count}')
    print(f'Ratio: {valid_count / (valid_count + invalid_count)}')


def sep_valid_invalid(in_file: str, valid_out_file: str, invalid_out_file: str):
    valid_file = open(valid_out_file, 'w')
    invalid_file = open(invalid_out_file, 'w')

    valid_count = 0
    invalid_count = 0

    with open(in_file, 'r') as f:
        line = f.readline()
        while line:
            if line_valid(line):
                valid_file.write(line)
                valid_count += 1
            else:
                invalid_file.write(line)
                invalid_count += 1

            line = f.readline()

    print(f'Valid Line Count: {valid_count}')
    print(f'Invalid Line Count: {invalid_count}')
    print(f'Valid Line Ratio: {valid_count / (valid_count + invalid_count)}')


def main(fix: bool, in_file: str, valid_out_file: str, invalid_out_file: str):
    if fix:
        fix_invalid(in_file, valid_out_file, invalid_out_file)
    else:
        sep_valid_invalid(in_file, valid_out_file, invalid_out_file)


if __name__ == '__main__':
    Fire(main)
