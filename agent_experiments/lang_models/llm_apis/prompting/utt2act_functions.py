"""
Functions which convert instances from datasethandler and corresponding annotatins from llms into string (line) outputs
for raw dataset files
"""
"""
Functions which convert instances from dataset handlers into a set of annotation prompts for llms
"""

from data.conversion.fs_examples import *

from simple_utils import remove_prefix

def utility_eg_formatter(value):
    if isinstance(value, str):
        return f'(E.g., {value})'

    # Otherwise handle dict case
    return f'(For example: {", and".join([f"{v} would be annotated {k}" for k, v in value.items()])})'


# Direct copy from inst2p function
def dnd_fs(inst):
    system_msg = {
        'role': 'system',
        'content': 
'''You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue.
User requests will contain the context which gives the number of each item available and the utterance to be annotated.
Respond to user requests succinctly, giving only the annotation, without extra words.
This is a list of possible annotation labels with descriptions. Note that "<slot>" indicates optional values that are filled based on the utterance:
"greet" - greeting the partner or small talk.
"inquire <slot>" - asking about partner's preferences. For example, 'CONTEXT: "2 books 2 hats 1 balls" UTTERANCE: "what would you like?"' would be annotated "inquire". 'CONTEXT: "1 books 1 hats 3 balls" UTTERANCE: "do you want the hat?"'" would be annotated "inquire hats".
"propose <slot>" - proposes an offer. Slots are filled based on what the speaker gets. For example, 'CONTEXT: "1 books 4 hats 1 balls" UTTERANCE: "i would like 4 hats and you can have the rest"' would be labeled "propose books=0 hats=4 balls=0". 'CONTEXT: "1 books 3 hats 1 balls" UTTERANCE: "you can have all three hats if i get the ball and book"' would be labeled "propose books=1 hats=0 balls=1".
"insist <slot>" - insists on a previous deal. For example, 'CONTEXT: "1 books 1 hats 4 balls" UTTERANCE: "no, i really need 2 of the balls"' would be annotated "insist balls=2".
"disagree" - implies disagreement or dissatisfaction with a deal.
"agree" - showing agreement to a deal or proposal. For example, the utterances "deal" or "yes" would both be annotated "agree".
"unknown" - the utterance does not fit any of the above labels.'''
    }
    
    item_counts = inst['ctx']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[1]} hats and {item_counts[2]} balls are available"'

    # Since value is not important here for generating action
    curr_utt = inst['read_inpt']
    
    act_prompt = [system_msg, {'role': 'user', 'content': f' Given this context: \n{ctx_str}\n What is the annotation for this utterance? UTTERANCE: "{curr_utt}"'}]
    return act_prompt

def casino_cust_form_fs(inst):
    system_msg = {
        'role': 'system',
        'content': 
'''You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood. 
Respond to user requests succinctly, giving only the annotation, without extra words. 
An utterance may have multiple correct annotations.'
This is a list of possible annotation labels with descriptions. Note that "<slot>" indicates optional values that are filled based on the utterance.:
"smalltalk" - greeting the partner or small talk.
"empathy coordination" - promotes coordination or friendliness between the speaker and their partner. 
"elicit preference <slot>" - asks about partner preferences. For example, "what items do you want most?" would be annotated "elicit preference", while "How much firewood do you want?" would be labeled "elicit preference firewood".
"no need <slot>" - a specific item is not important to the speaker. For example, "we already have plenty of water" would be annotated "no need water".
"undervalue <slot>" - attempts to convince a partner a particular item is less important. For example, "Do you have help carrying all that extra firewood? Could be heavy" would be annotated "undervalue firewood".
"vouch fairness" - vouches for the fairness of a deal or proposal.
"express preference <slot>" - implies the speaker's preference for an item. For example, "I really need food" would be annotated "express preference food".
"propose <slot>" - proposes an offer. Slots are filled based on what the speaker of the utterance gets. For example, "How about I get 2 water and you get all the food" would be labeled "propose food=0 water=2". "you can have all three water if i get all the food and firewood" would be annotated "propose food=3 water=0 firewood=3". "yes, I get 2 food 3 water and 1 firewood and you get 1 food and 2 firewood" would be annotated "propose food=2 water=3 firewood=1" because the speaker receives 2 food, 3 water, and  1 firewood. "OK, you get 1 Food, 1 firewood and 3 waters" would be annotated "propose food=2 water=0 firewood=2" because after the partner gets their items there would be 2 food, 0 water, and 2 firewood for the speaker to receive.
"disagree" - implies disagreement or dissatisfaction with a deal.
"agree" - showing agreement to a deal or proposal. For example, the utterances "deal" or "Submit-Deal" would both be annotated "agree".
"unknown" - the utterance does not fit any of the above labels.'''
    }
    
    item_counts = inst['ctx']
    print()
    # reason = " ".join(inst["ctx"][inst["ctx"].index("=")+1:])
    reason = ""
    ctx_str = f'CONTEXT: "{item_counts[0]} firewoods {item_counts[2]} water {item_counts[4]} food"' + reason
    curr_utt = inst['read_inpt']

    act_prompt = [system_msg, {'role': 'user', 'content': f'Given this context: \n{ctx_str}\n What is the annotation for this utterance? UTTERANCE: "{curr_utt}"'}]
    return act_prompt

# def casino_dnd_form_fs(inst):
#     system_msg = {
#         'role': 'system',
#         'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue. Respond to user requests succinctly, giving only the annotation, without extra words. Possible annotations are: "Empathy/Coordination", "Undervalue Partner", "Non-strategic", "Small Talk", "No-need", "Vouch Fairness", "Self/Other Need", "Elicit Preferences"'
#         }
#     user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n ' + ' '.join([f'UTTERANCE: "{t}\n" ANNOTATION: "{a}"' for t, a in zip(casino_dnd_format_examples, casino_dnd_format_annots)])
#     item_counts = inst['ctx']
#     reason = " ".join(inst["ctx"][inst["ctx"].index("=")+1:])
#     ctx_str = f'CONTEXT: "{item_counts[0]} firewood {item_counts[2]} water {item_counts[4]} food"' + reason
#     curr_utt = inst['read_inpt']

#     act_prompt = [system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{curr_utt}"'])}]
#     return act_prompt

# Finalized versions

def final_utt2act_dnd(inst):
    system_msg = {
        'role': 'system',
        'content': 
'''You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue.
User requests will contain the context which gives the number of each item available and the utterance to be annotated.
Respond to user requests succinctly, giving only the annotation, without extra words.
This is a list of possible annotation labels with descriptions. Note that "<slot>" indicates optional values that are filled based on the utterance:
"greet" - greeting the partner or small talk.
"inquire <slot>" - asking about partner's preferences. For example, 'CONTEXT: "2 books 2 hats 1 balls" UTTERANCE: "what would you like?"' would be annotated "inquire". 'CONTEXT: "1 books 1 hats 3 balls" UTTERANCE: "do you want the hat?"'" would be annotated "inquire hats".
"propose <slot>" - proposes an offer. Slots are filled based on what the speaker gets. For example, 'CONTEXT: "1 books 4 hats 1 balls" UTTERANCE: "i would like 4 hats and you can have the rest"' would be labeled "propose books=0 hats=4 balls=0". 'CONTEXT: "1 books 3 hats 1 balls" UTTERANCE: "you can have all three hats if i get the ball and book"' would be labeled "propose books=1 hats=0 balls=1".
"insist <slot>" - insists on a previous deal. For example, 'CONTEXT: "1 books 1 hats 4 balls" UTTERANCE: "no, i really need 2 of the balls"' would be annotated "insist balls=2".
"disagree" - implies disagreement or dissatisfaction with a deal.
"agree" - showing agreement to a deal or proposal. For example, the utterances "deal" or "yes" would both be annotated "agree".
"unknown" - the utterance does not fit any of the above labels.'''
    }
    
    ctx_str = f'CONTEXT: "{inst["ctx"][0]} books {inst["ctx"][2]} hats and {inst["ctx"][4]} balls are available"'

    return [[system_msg, {'role': 'user', 'content': f'Given this context: \n{ctx_str}\n What is the annotation for this utterance?\nUTTERANCE: "{inst["read_inpt"]}"'}]]

def final_utt2act_casino_cust(inst):
    system_msg = {
        'role': 'system',
        'content': 
'''You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood. 
Respond to user requests succinctly, giving only the annotation, without extra words. 
An utterance may have multiple correct annotations.'
This is a list of possible annotation labels with descriptions. Note that "<slot>" indicates optional values that are filled based on the utterance.:
"smalltalk" - greeting the partner or small talk.
"empathy coordination" - promotes coordination or friendliness between the speaker and their partner. 
"elicit preference <slot>" - asks about partner preferences. For example, "what items do you want most?" would be annotated "elicit preference", while "How much firewood do you want?" would be labeled "elicit preference firewood".
"no need <slot>" - a specific item is not important to the speaker. For example, "we already have plenty of water" would be annotated "no need water".
"undervalue <slot>" - attempts to convince a partner a particular item is less important. For example, "Do you have help carrying all that extra firewood? Could be heavy" would be annotated "undervalue firewood".
"vouch fairness" - vouches for the fairness of a deal or proposal.
"express preference <slot>" - implies the speaker's preference for an item. For example, "I really need food" would be annotated "express preference food".
"propose <slot>" - proposes an offer. Slots are filled based on what the speaker of the utterance gets. For example, "How about I get 2 water and you get all the food" would be labeled "propose food=0 water=2". "you can have all three water if i get all the food and firewood" would be annotated "propose food=3 water=0 firewood=3". "yes, I get 2 food 3 water and 1 firewood and you get 1 food and 2 firewood" would be annotated "propose food=2 water=3 firewood=1" because the speaker receives 2 food, 3 water, and  1 firewood. "OK, you get 1 Food, 1 firewood and 3 waters" would be annotated "propose food=2 water=0 firewood=2" because after the partner gets their items there would be 2 food, 0 water, and 2 firewood for the speaker to receive.
"disagree" - implies disagreement or dissatisfaction with a deal.
"agree" - showing agreement to a deal or proposal. For example, the utterances "deal" or "Submit-Deal" would both be annotated "agree".
"unknown" - the utterance does not fit any of the above labels.'''
    }

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{inst["read_inpt"]}"'}]]


def reduced_casino_cust_format(inst):
    system_msg = {
        'role': 'system',
        'content': 
'''You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood. 
Respond to user requests succinctly, giving only the annotation, without extra words. 
An utterance may have multiple correct annotations.'
This is a list of possible annotation labels with descriptions. Note that "<slot>" indicates optional values that are filled based on the utterance.:
"smalltalk" - greeting the partner or small talk.
"elicit preference <slot>" - asks about partner preferences. For example, "what items do you want most?" would be annotated "elicit preference", while "How much firewood do you want?" would be labeled "elicit preference firewood".
"no need <slot>" - a specific item is not important to the speaker. For example, "we already have plenty of water" would be annotated "no need water".
"express preference <slot>" - implies the speaker's preference for an item. For example, "I really need food" would be annotated "express preference food".
"propose <slot>" - proposes an offer. Slots are filled based on what the speaker of the utterance gets. For example, "How about I get 2 water and you get all the food" would be labeled "propose food=0 water=2". "you can have all three water if i get all the food and firewood" would be annotated "propose food=3 water=0 firewood=3". "yes, I get 2 food 3 water and 1 firewood and you get 1 food and 2 firewood" would be annotated "propose food=2 water=3 firewood=1" because the speaker receives 2 food, 3 water, and  1 firewood. "OK, you get 1 Food, 1 firewood and 3 waters" would be annotated "propose food=2 water=0 firewood=2" because after the partner gets their items there would be 2 food, 0 water, and 2 firewood for the speaker to receive.
"disagree" - implies disagreement or dissatisfaction with a deal.
"agree" - showing agreement to a deal or proposal. For example, the utterances "deal" or "Submit-Deal" would both be annotated "agree".
"unknown" - the utterance does not fit any of the above labels.'''
    }

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{inst["read_inpt"]}"'}]]

