"""
Functions which convert instances from dataset handlers into a set of annotation prompts for llms
"""

from data.conversion.fs_examples import *


def example_inst2p_func(inst):  # Just for casino dataset, returns "annotate this: {utterance}"
    # print(inst)
    # print(type(inst))
    return [f"annotate this: {chat_item['text']}" for chat_item in inst['chat_logs']]


def format_prompt(strg):
        prompt_str = "Predict the annotation for the last utterance by following the similar format as provided. "
        # format the utterance
        strg = "utterance: " + strg + "<eos> " + "annotation: "
        strg = prompt_str + strg
        return strg


def completion_dnd_annot_prompt_fun(inst):
    start_str = 'Choose the best simple annotation for these utterances in a negotiation dialogue, given the context of how many of each item is available:'
    annot_labels_str = 'Possible annotations are: "greet", "inquire:, "propose", "disagree", "insist", and "agree"'

    fs_examples_str = '\n'.join([f'{t}\nANNOTATION: "{a}"' for t, a in zip(dnd_fs_texts, dnd_fs_annots_no_vc)])
    
    splt_dia = [u.lstrip('YOU: ').lstrip('THEM: ') for u in inst['dialogue'].split(' <eos> ')]
    item_counts = inst['input']['count']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[1]} hats {item_counts[2]} balls"'
    
    return ['\n'.join([start_str, annot_labels_str, fs_examples_str, f'{ctx_str} UTTERANCE: "{u}"\nAnnotation: ']) for u in splt_dia]


def chat_dnd_annot_prompt_fun(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue, given the context of how many of each item is available. Possible annotations are: "greet", "inquire:, "propose", "disagree", "insist", and "agree"'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'{t}\nANNOTATION: "{a}"' for t, a in zip(dnd_fs_texts, dnd_fs_annots_no_vc)])

    splt_dia = [u.lstrip('YOU: ').lstrip('THEM: ') for u in inst['dialogue'].split(' <eos> ')]
    item_counts = inst['input']['count']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[1]} hats {item_counts[2]} balls"'

    return [[system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{u}"'])}] for u in splt_dia]


# Annotates at selected/refined L2 act level
def completion_casino_annot_prompt_fun(inst):
    start_str = 'Choose the annotation label for these utterances in a negotiation dialogue.\nPossible annotations are: "Empathy/Coordination", "Undervalue Partner", "Non-strategic", "Small Talk", "No-need", "Vouch Fairness", "Self/Other Need", "Elicit Preferences"'

    fs_examples_str = '\n'.join([f'UTTERANCE: "{t}"\nANNOTATION: "{a}"' for t, a in zip(casino_fs_texts, casino_fs_annots_l2_selref)])
    
    splt_dia = [u.lstrip('YOU: ').lstrip('THEM: ') for u in inst['dialogue'].split(' <eos> ')]
    
    return ['\n'.join([start_str, fs_examples_str, f'UTTERANCE: "{u}"\nAnnotation: ']) for u in splt_dia]


# Annotates at selected/refined L2 act level
# TODO
def chat_casino_annot_prompt_fun(inst):
    return ''


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
