from fire import Fire
import json
from datasets import load_dataset

N = 20


def do_dnd(f_path):
    ds = load_dataset("deal_or_no_dialog")

    i = 0
    results = []
    for s in ds['train'].select(range(N)):
        print()
        print(i)
        i += 1

        utts = s['dialogue'].split(' <eos> ')
        annots = []
        
        counts = s['input']['count']
        ctx = f'books={counts[0]} hats={counts[1]} balls={counts[2]}'
        dialogue = ''
        for u in utts:
            print('\nCONTEXT:')
            print(ctx)
            print('DIALOGUE HISTORY:')
            print(dialogue)
            print('\nANNOTATE THIS:')
            print(u)

            annots.append(input())
            dialogue += f'\n{u}'

        results.append([(u, a) for u, a in zip(utts, annots)])
    
    with open(f_path, 'w') as f:
        f.write(json.dumps(results))


def do_casino(f_path):
    ds = load_dataset("casino")

    i = 0
    results = []
    for s in ds['train'].select(range(N)):
        print()
        print(i)
        i += 1

        utts = [u['text'] for u in s['chat_logs']]
        annots = []

        dialogue = ''
        for u in utts:
            print('\nCONTEXT:\nfood=3 water=3 firewood=3')
            print('DIALOGUE HISTORY:')
            print(dialogue)
            print('\nANNOTATE THIS:')
            print(u)

            annots.append(input().split(', '))
            dialogue += f'\n{u}'

        results.append([(u, a) for u, a in zip(utts, annots)])
    
    with open(f_path, 'w') as f:
        f.write(json.dumps(results))


def main():
    # print('ANNOTATE DND UTTERANCES:\n')
    # do_dnd('dnd_valset.json')

    # print('ANNOTATE CASINO UTTERANCES (dnd format):\n')
    # do_casino('casino_dndform_valset.json')

    print('ANNOTATE CASINO UTTERANCES (custom format):\n')
    do_casino('casino_customform_valset.json')


if __name__ == '__main__':
    Fire(main)

'''
DND FORMAT: 

Greet
Inquire [w slots]
    Slots Example: Inquire hats
    Multi-Issue Slots Example: Inquire books balls
    Could also have no slots. E.g., “What items do you want?” → “inquire”
Propose [w slots]
    Slots Example: Propose books=0 hats=1 balls=3
    Partial proposal: Propose hats=1
Disagree
Insist
    Slots Example: Insist books=0 hats=1 balls=3
    Do we need slots here? Information should be kind of in past dialogue act labels if we provide that I think
    Going with no slots for now, simplifies schema and generally does not lose information because of this.
Agree
Unknown/NA
    No FS example needed, can express this option in prompt
'''

'''
CUSTOM CASINO FORMAT: 

Small-talk --> smalltalk
Empathy/Coordination --> empathy coordination
No-need [w slots] --> no need
    Slots Example: No-need water
Elicit Preference [w slots] --> elicit preference
    Slots Example: Elicit Preference food
    Multi-Issue Slots Example: Elicit Preference food water
Undervalue Partner [w slots] --> undervalue
    Slots Example: Undervalue firewood
    Important but kind of a subtle, will need good prompts/fs examples
Vouch Fairness --> vouch fairness
Express preference [w slots] --> express preference
    Slots Example: Express Preference food
    Multi-Issue Slots Example: Express Preference food water
    Originally called Self/Other Need
Propose [w slots] --> propose
    Slots Example: Propose food=0 water=1 firewood=3
    Partial proposal: Propose firewood=1
Disagree
Agree
Unknown/NA --> unknown


No, if you get 2 food, it's only fair that I get 2 firewood.  --> should be insist

ANNOTATE THIS:
Accept-Deal
agree
'''
