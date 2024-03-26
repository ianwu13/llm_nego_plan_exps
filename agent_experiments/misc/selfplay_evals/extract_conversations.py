import json
import re

import argparse


def process_prefs(alice_pref, bob_pref):
    # Alice : firewood=(count:3 value:3) water=(count:3 value:5) food=(count:3 value:4)
    # Bob   : firewood=(count:3 value:3) water=(count:3 value:5) food=(count:3 value:4)
    items = ['firewood', 'water', 'food']
    ap = {}
    bp = {}
    ic = {i: 3 for i in items}

    for i_data in alice_pref.split(': ')[1].split(') '):
        for i in items:
            if i_data.startswith(i):
                ap[i] = int(i_data.split(':')[-1].rstrip(')\n'))

    for i_data in bob_pref.split(': ')[1].split(') '):
        for i in items:
            if i_data.startswith(i):
                bp[i] = int(i_data.split(':')[-1].rstrip(')\n'))

    return ap, bp, ic


def check_line_deal(line):
    # Alice : firewood=1 water=2 food=1
    # Bob   : firewood=2 water=1 food=1
    pattern = re.compile("firewood=[0-9] water=[0-9] food=[0-9]")
    return pattern.match(line.split(' : ')[1])


def read_convo_json(f):
    alice_pref = f.readline()
    bob_pref = f.readline()

    ap, bp, ic = process_prefs(alice_pref, bob_pref)
    
    f.readline()
    convo_utts = []
    line = f.readline()
    while (not line.startswith('-----')) and (not line.startswith('=====')):
        convo_utts.append(line)
        line = f.readline()
    
    while not line.startswith('====='):
        line = f.readline()

    # Check if last 2 lines have a deal, remove if true
    if check_line_deal(convo_utts[-1]) and check_line_deal(convo_utts[-2]):
        convo_utts = convo_utts[:-2] 

    convo_json = {
        "alice_pref": ap,
        "bob_pref": bp,
        "item_counts": ic,
        "convo": convo_utts
    }
    return convo_json


def extract_convo_json_list(log_path):
    f = open(log_path, 'r')
    convo_json_list = []

    line = f.readline()
    while line != "":
        if line.startswith('====='):
            convo_json_list.append(read_convo_json(f))
        
        line = f.readline()

    f.close()
    return convo_json_list


def main():
    parser = argparse.ArgumentParser(description='script to annotate data')
    parser.add_argument('--infile', type=str,
        help='.log file to extract conversations from')
    parser.add_argument('--outfile', type=str,
        help='.json file to write conversations to')
    args = parser.parse_args()

    convo_json_list = extract_convo_json_list(args.infile)
    print(len(convo_json_list))

    with open(args.outfile, 'w') as f:
        json.dump(convo_json_list, f)


if __name__ == '__main__':
    main()
