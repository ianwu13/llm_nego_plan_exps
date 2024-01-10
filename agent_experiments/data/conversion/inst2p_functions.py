"""
Functions which convert instances from dataset handlers into a set of annotation prompts for llms
"""

from data.conversion.fs_examples import *

from simple_utils import remove_prefix


def example_inst2p_func(inst):  # Just for casino dataset, returns "annotate this: {utterance}"
    # print(inst)
    # print(type(inst))
    return [chat_item['text'] for chat_item in inst['chat_logs']]


def example_inst2p_func_dnd(inst):  # Just for casino dataset, returns "annotate this: {utterance}"
    # print(inst)
    # print(type(inst))
    return [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]


def format_prompt(strg):
        prompt_str = "Predict the annotation for the last utterance by following the similar format as provided. "
        # format the utterance
        strg = "utterance: " + strg + "<eos> " + "annotation: "
        strg = prompt_str + strg
        return strg


def completion_dnd_annot_prompt_fun(inst):
    start_str = 'Choose the best simple annotation for these utterances in a negotiation dialogue, given the context of how many of each item is available:'
    annot_labels_str = 'Possible annotations are: "greet", "inquire", "propose", "disagree", "insist", and "agree"'

    fs_examples_str = '\n'.join([f'{t}\nANNOTATION: "{a}"' for t, a in zip(dnd_fs_texts, dnd_fs_annots_no_vc)])
    
    splt_dia = [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]
    item_counts = inst['input']['count']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[1]} hats {item_counts[2]} balls"'
    
    return ['\n'.join([start_str, annot_labels_str, fs_examples_str, f'{ctx_str} UTTERANCE: "{u}"\nAnnotation: ']) for u in splt_dia]


def chat_dnd_annot_prompt_fun(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue, given the context of how many of each item is available. Possible annotations are: "greet", "inquire", "propose", "disagree", "insist", and "agree"'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'{t}\nANNOTATION: "{a}"' for t, a in zip(dnd_fs_texts, dnd_fs_annots_no_vc)])

    splt_dia = [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]
    item_counts = inst['input']['count']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[1]} hats {item_counts[2]} balls"'

    return [[system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{u}"'])}] for u in splt_dia]


# Annotates at selected/refined L2 act level
def completion_casino_annot_prompt_fun(inst):
    start_str = 'Choose the annotation label for these utterances in a negotiation dialogue.\nPossible annotations are: "Empathy/Coordination", "Undervalue Partner", "Non-strategic", "Small Talk", "No-need", "Vouch Fairness", "Self/Other Need", "Elicit Preferences"'

    fs_examples_str = '\n'.join([f'UTTERANCE: "{t}"\nANNOTATION: "{a}"' for t, a in zip(casino_fs_texts, casino_fs_annots_l2_selref)])
    
    return ['\n'.join([start_str, fs_examples_str, f'UTTERANCE: "{u["text"]}"\nAnnotation: ']) for u in inst['chat_logs']]


# Annotates at selected/refined L2 act level
def chat_casino_annot_prompt_fun(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue.\nPossible annotations are: "Empathy/Coordination", "Undervalue Partner", "Non-strategic", "Small Talk", "No-need", "Vouch Fairness", "Self/Other Need", "Elicit Preferences"'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'UTTERANCE: "{t}"\nANNOTATION: "{a}"' for t, a in zip(casino_fs_texts, casino_fs_annots_l2_selref)])

    return [[system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance?\nUTTERANCE: "{u["text"]}"'])}] for u in inst['chat_logs']]


# split utterance seperately
def utters_split_seperate(line):
    # without the final selection
    utters_list = []
    for i in range (0, len(line.split("<eos>"))):
        each = line.split("<eos>")[i]
        each = format_prompt(each)
        utters_list.append(each)
    return utters_list


def demo_dnd(inst):
    # extract utterances
    dialogue_str = inst['dialogue']
    prompt_list = utters_split_seperate(dialogue_str )
    return prompt_list


def demo_casino(inst):
    # print(inst)
    prompt_list = []
    for each in inst['chat_logs']:
        prompt_intro = "annotate this : "
        prompt = prompt_intro + f"{each['id']}: {each['text']}"
        prompt_list.append(prompt)
    # print(prompt_list)
    return prompt_list


# FINAL FUNCTIONS - All Chat


def utility_eg_formatter(value):
    if isinstance(value, str):
        return f'(For example, {value})'

    # Otherwise handle dict case
    return f'(For example: {", and ".join([f"{v} would be annotated {k}" for k, v in value.items()])})'


def utility_eg_formatter_beta(key, value):
    if isinstance(value, str):
        return f'{value}: {key}\n'

    # Otherwise handle dict case
    return ''.join([f'{v}: {k}\n' for k, v in value.items()])


def final_dnd_fs(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue. Possible annotations are: "greet", "inquire", "propose", "disagree", "insist", "agree", and "unknown"'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'{t}\nANNOTATION: "{a}"' for t, a in zip(dnd_fs_examples, dnd_annots)])

    splt_dia = [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]
    item_counts = inst['input']['count']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[1]} hats {item_counts[2]} balls"'

    return [[system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{u}"'])}] for u in splt_dia]


def final_dnd_example(inst):
    system_msg = {
        'role': 'system',
        'content': f'You are assisting the user in annotating utterances in a negotiation dialogue. Respond to user requests succinctly, giving only the annotation, without extra words. Possible annotations are: {", ".join([f"{k} {utility_eg_formatter(v)}" for k, v in dnd_rb_format.items()])}, and "Unknown"'
        }

    splt_dia = [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{u}"'}] for u in splt_dia]


def final_casino_dnd_form_fs(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue.\nPossible annotations are: "Empathy/Coordination", "Undervalue Partner", "Non-strategic", "Small Talk", "No-need", "Vouch Fairness", "Self/Other Need", "Elicit Preferences"'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'UTTERANCE: "{t}"\nANNOTATION: "{a}"' for t, a in zip(casino_dnd_format_examples, casino_dnd_format_annots)])

    return [[system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance?\nUTTERANCE: "{u["text"]}"'])}] for u in inst['chat_logs']]


def final_casino_dnd_form_example(inst):
    system_msg = {
        'role': 'system',
        'content': f'You are assisting the user in annotating utterances in a negotiation dialogue for dividing 3 units each of food, water, and firewood. Respond to user requests succinctly, giving only the annotation, without extra words. Possible annotations are: {", ".join([f"{k} {utility_eg_formatter(v)}" for k, v in casino_dnd_format.items()])}, and "Unknown"'
        }

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{u["text"]}"'}] for u in inst['chat_logs']]


def final_casino_cust_form_fs(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood.\nPossible annotations are: "Empathy/Coordination", "Undervalue Partner", "Non-strategic", "Small Talk", "No-need", "Vouch Fairness", "Self/Other Need", "Elicit Preferences". A single input (utterance) may have multiple correct annotations.'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'UTTERANCE: "{t}"\nANNOTATION: "{a}"' for t, a in zip(casino_cust_format_examples, casino_cust_format_multilab_annots)])

    return [[system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance?\nUTTERANCE: "{u["text"]}"'])}] for u in inst['chat_logs']]


def final_casino_cust_form_example(inst):
    system_msg = {
        'role': 'system',
        'content': f'You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood. Respond to user requests succinctly, giving only the annotation, without extra words. Possible annotations are: {", ".join([f"{k} {utility_eg_formatter(v)}" for k, v in casino_cust_format.items()])}, and "Unknown". A single input (utterance) may have multiple correct annotations.'
        }

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{u["text"]}"'}] for u in inst['chat_logs']]


# NO FS PROMPT FUNCTIONS
def final_dnd_no_fs(inst):
    system_msg = {
        'role': 'system',
        'content': '''You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue.
User requests will contain the context which gives the number of each item available and the utterance to be annotated.
Respond to user requests succinctly, giving only the annotation, without extra words. 
This is a list of possible annotation labels with descriptions:
"greet" - the utterance is a greeting or smalltalk.
"inquire" - the utterance is inquiring about items. This can be a general inquiry such as "what items do you want most?" or about a specific item such as "How many balls do you want?". In the second case, the label would be "inquire balls".
"propose" - the utterance proposes a deal. For example, "How about I get 2 balls and you get all the hats" would be labeled "propose hats=0 balls=2". Note that the values in the label are for how much of each item the speaker gets, not their partner.
"disagree" - the utterance is disagreeing with the last utterance or a proposed deal.
"insist" - the user insists on a deal. This label has similar slots to "propose". For example, "No I really need 2 hats" would be annotated "insist hats=2".
"agree" - the utterance is agreeing.
"unknown" - the utterance does not not fit into any of the provided labels'''
        }
    # user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'{t}\nANNOTATION: "{a}"' for t, a in zip(dnd_fs_examples, dnd_annots)])

    splt_dia = [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]
    item_counts = inst['input']['count']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[1]} hats {item_counts[2]} balls"'

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this context and utterance? {ctx_str} UTTERANCE: "{u}"'}] for u in splt_dia]


def final_casino_dnd_form_no_fs(inst):
    system_msg = {
        'role': 'system',
        'content': '''You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood. 
Respond to user requests succinctly, giving only the annotation, without extra words. 
A single input (utterance) may have multiple correct annotations.'
This is a list of possible annotation labels with descriptions:
"greet" - the utterance is a greeting or smalltalk.
"inquire" - the utterance is inquiring about items. This can be a general inquiry such as "what items do you want most?" or about a specific item such as "How much firewood do you want?". In the second case, the label would be "inquire firewood".
"propose" - the utterance proposes a deal. For example, "How about I get 2 food and you get all the water" would be labeled "propose food=2 water=0". Note that the values in the label are for how much of each item the speaker gets, not their partner.
"insist" - the user insists on a deal. This label has similar slots to "propose". For example, "No I really need 2 water" would be annotated "insist water=2".
"disagree" - the utterance is disagreeing with the last utterance or a proposed deal.
"agree" - the utterance is agreeing.
"unknown" - the utterance does not not fit into any of the provided labels'''
        }

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{u["text"]}"'}] for u in inst['chat_logs']]


def final_casino_cust_form_no_fs(inst):
    system_msg = {
        'role': 'system',
        'content': f'''You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood. 
Respond to user requests succinctly, giving only the annotation, without extra words. 
A single input (utterance) may have multiple correct annotations.'
This is a list of possible annotation labels with descriptions:
"smalltalk" - the utterance is a greeting or smalltalk.
"empathy coordination" - the utterance promotes coordination/friendliness between the speaker and their partner. 
"elicit preference" - the utterance attempts to gain information about partner preferences. This can be a general inquiry such as "what items do you want most?" or about a specific item such as "How much firewood do you want?". In the second case, the label would be "elicit preference firewood".
"no need" - the utterance indicates that there the speaker does not need a specific item. For example, "we already have plenty of water" would be annotated "no need water".
"undervalue" - the utterance attempts to influence the partner's preference for an item. For example, "Do you have help carrying all that extra firewood? Could be heavy" would be annotated "undervalue firewood".
"vouch fairness" - the utterance vouches for the fairness of a deal or proposal.
"express preference" - the utterance expresses the speakers preference for an item. For example, "I really need food" would be annotated "express preference food".
"propose" - the utterance proposes a deal. For example, "How about I get 2 food and you get all the water" would be labeled "propose food=2 water=0". Note that the values in the label are for how much of each item the speaker gets, not their partner.
"disagree" - the utterance is disagreeing with the last utterance or a proposed deal.
"agree" - the utterance is agreeing.
"unknown" - the utterance does not not fit into any of the provided labels'''
        }

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{u["text"]}"'}] for u in inst['chat_logs']]


# DESCRIPTION AND FS PROMPT FUNCTIONS
def final_dnd_desc_fs(inst):
    system_msg = {
        'role': 'system',
        'content': 
'''You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue.
User requests will contain the context which gives the number of each item available and the utterance to be annotated.
Respond to user requests succinctly, giving only the annotation, without extra words. 
This is a list of possible annotation labels with descriptions:
"greet" - the utterance is a greeting or smalltalk.
"inquire" - the utterance is inquiring about items. This can be a general inquiry such as "what items do you want most?" or about a specific item such as "How many balls do you want?". In the second case, the label would be "inquire balls".
"propose" - the utterance proposes a deal. For example, "How about I get 2 balls and you get all the hats" would be labeled "propose hats=0 balls=2". Note that the values in the label are for how much of each item the speaker gets, not their partner.
"disagree" - the utterance is disagreeing with the last utterance or a proposed deal.
"insist" - the user insists on a deal. This label has similar slots to "propose". For example, "No I really need 2 hats" would be annotated "insist hats=2".
"agree" - the utterance is agreeing.
"unknown" - the utterance does not not fit into any of the provided labels'''
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'{t}\nANNOTATION: "{a}"' for t, a in zip(dnd_fs_examples, dnd_annots)])

    splt_dia = [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]
    item_counts = inst['input']['count']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[1]} hats {item_counts[2]} balls"'

    return [[system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{u}"'])}] for u in splt_dia]


def final_casino_dnd_form_desc_fs(inst):
    system_msg = {
        'role': 'system',
        'content': '''You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood. 
Respond to user requests succinctly, giving only the annotation, without extra words. 
A single input (utterance) may have multiple correct annotations.'
This is a list of possible annotation labels with descriptions:
"greet" - the utterance is a greeting or smalltalk.
"inquire" - the utterance is inquiring about items. This can be a general inquiry such as "what items do you want most?" or about a specific item such as "How much firewood do you want?". In the second case, the label would be "inquire firewood".
"propose" - the utterance proposes a deal. For example, "How about I get 2 food and you get all the water" would be labeled "propose food=2 water=0". Note that the values in the label are for how much of each item the speaker gets, not their partner.
"insist" - the user insists on a deal. This label has similar slots to "propose". For example, "No I really need 2 water" would be annotated "insist water=2".
"disagree" - the utterance is disagreeing with the last utterance or a proposed deal.
"agree" - the utterance is agreeing.
"unknown" - the utterance does not not fit into any of the provided labels'''
        }

    return [[system_msg, {'role': 'user', 'content': f'Here are some examples of how annotations should look:\n{"".join([utility_eg_formatter_beta(k, v) for k, v in casino_dnd_format.items()])}\nWhat is the annotation for this utterance? "{u["text"]}"'}] for u in inst['chat_logs']]


def final_casino_cust_form_desc_fs(inst):
    system_msg = {
        'role': 'system',
        'content': '''You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood. 
Respond to user requests succinctly, giving only the annotation, without extra words. 
A single input (utterance) may have multiple correct annotations.'
This is a list of possible annotation labels with descriptions:
"smalltalk" - the utterance is a greeting or smalltalk.
"empathy coordination" - the utterance promotes coordination/friendliness between the speaker and their partner. 
"elicit preference" - the utterance attempts to gain information about partner preferences. This can be a general inquiry such as "what items do you want most?" or about a specific item such as "How much firewood do you want?". In the second case, the label would be "elicit preference firewood".
"no need" - the utterance indicates that there the speaker does not need a specific item. For example, "we already have plenty of water" would be annotated "no need water".
"undervalue" - the utterance attempts to influence the partner's preference for an item. For example, "Do you have help carrying all that extra firewood? Could be heavy" would be annotated "undervalue firewood".
"vouch fairness" - the utterance vouches for the fairness of a deal or proposal.
"express preference" - the utterance expresses the speakers preference for an item. For example, "I really need food" would be annotated "express preference food".
"propose" - the utterance proposes a deal. For example, "How about I get 2 food and you get all the water" would be labeled "propose food=2 water=0". Note that the values in the label are for how much of each item the speaker gets, not their partner.
"disagree" - the utterance is disagreeing with the last utterance or a proposed deal.
"agree" - the utterance is agreeing.
"unknown" - the utterance does not not fit into any of the provided labels'''
        }

    return [[system_msg, {'role': 'user', 'content': f'Here are some examples of how annotations should look:\n{"".join([utility_eg_formatter_beta(k, v) for k, v in casino_cust_format.items()])}\nWhat is the annotation for this utterance? "{u["text"]}"'}] for u in inst['chat_logs']]

# OLD

def casino_dnd_format_testing(inst):
    system_msg = {
        'role': 'system',
        'content': 
'''You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood. 
User requests will contain the context which gives the number of each item available and the utterance to be annotated.
Respond to user requests succinctly, giving only the annotation, without extra words. 
This is a list of possible annotation labels with descriptions. Note that "<slot>" indicates optional values that are filled based on the utterance.:
"greet" - greeting the partner or small talk.
"inquire <slot>" - asking about partner's preferences. For example, "what items do you want most?" would be annotated "inquire". "How much firewood do you want?" would be annotated "inquire firewood".
"propose <slot>" - proposes an offer. Slots are filled based on what the speaker gets. For example, "How about I get 2 water and you get all the food" would be labeled "propose food=0 water=2", and "i will give you that in exchange for 1 food and 3 water with 2 firewood" would be annotated "propose food=1 water=3 firewood=2". "you can have all three water if i get the food and firewood" would be annotated "propose food=3 water=0 firewood=3".
"insist <slot>" - insists on a previous deal. For example, "No, I really need 2 firewood" would be annotated "insist firewood=2".
"disagree" - expressing disagreement or dissatisfaction with a deal.
"agree" - showing agreement to a deal or proposal. For example, the utterances "deal" or "Submit-Deal" would both be annotated "agree".
"unknown" - the utterance does not fit any of the above labels.'''
    }

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{u["text"]}"'}] for u in inst['chat_logs']]

# FINAL

def finalized_dnd(inst):
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
    
    splt_dia = [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]
    item_counts = inst['input']['count']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[1]} hats and {item_counts[2]} balls are available"'

    return [[system_msg, {'role': 'user', 'content': f'Given this context: \n{ctx_str}\n What is the annotation for this utterance?\nUTTERANCE: "{u}"'}] for u in splt_dia]


# CURRENT FINAL
def finalized_casino_cust_format(inst):
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
"propose <slot>" - proposes an offer. Slots are filled based on what the speaker of the utterance gets. For example, "How about I get 2 water and you get all the food" would be labeled "propose food=0 water=2". "you can have all three water if i get all the food and firewood" would be annotated "propose food=3 water=0 firewood=3". "yes, I get 2 food 3 water and 1 firewood and you get 1 food and 2 firewood" would be annotated "propose food=2 water=3 firewood=1" because the speaker recieves 2 food, 3 water, and  1 firewood. "OK, you get 1 Food, 1 firewood and 3 waters" would be annotated "propose food=2 water=0 firewood=2" because after the partner gets their items there would be 2 food, 0 water, and 2 firewood for the speaker to recieve.
"disagree" - implies disagreement or dissatisfaction with a deal.
"agree" - showing agreement to a deal or proposal. For example, the utterances "deal" or "Submit-Deal" would both be annotated "agree".
"unknown" - the utterance does not fit any of the above labels.'''
    }

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{u["text"]}"'}] for u in inst['chat_logs']]


# DRAFT
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
"propose <slot>" - proposes an offer. Slots are filled based on what the speaker of the utterance gets. For example, "How about I get 2 water and you get all the food" would be labeled "propose food=0 water=2". "you can have all three water if i get all the food and firewood" would be annotated "propose food=3 water=0 firewood=3". "yes, I get 2 food 3 water and 1 firewood and you get 1 food and 2 firewood" would be annotated "propose food=2 water=3 firewood=1" because the speaker recieves 2 food, 3 water, and  1 firewood. "OK, you get 1 Food, 1 firewood and 3 waters" would be annotated "propose food=2 water=0 firewood=2" because after the partner gets their items there would be 2 food, 0 water, and 2 firewood for the speaker to recieve.
"disagree" - implies disagreement or dissatisfaction with a deal.
"agree" - showing agreement to a deal or proposal. For example, the utterances "deal" or "Submit-Deal" would both be annotated "agree".
"unknown" - the utterance does not fit any of the above labels.'''
    }

    return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{u["text"]}"'}] for u in inst['chat_logs']]