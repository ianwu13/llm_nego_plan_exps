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


def dnd_fs(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue. Possible annotations are: "greet", "inquire:, "propose", "disagree", "insist", and "agree"'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'{t}\n ANNOTATION: "{a}"' for t, a in zip(dnd_fs_examples, dnd_annots)])
    item_counts = inst['ctx']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[2]} hats {item_counts[4]} balls"'
    # Since value is not important here for generating action
    curr_utt = inst['read_inpt']
    act_prompt = [system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f' What is the annotation for this utterance? {ctx_str} UTTERANCE: "{curr_utt}"'])}]
    return act_prompt

def casino_dnd_form_fs(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue. Respond to user requests succinctly, giving only the annotation, without extra words. Possible annotations are: "Empathy/Coordination", "Undervalue Partner", "Non-strategic", "Small Talk", "No-need", "Vouch Fairness", "Self/Other Need", "Elicit Preferences"'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n ' + ' '.join([f'UTTERANCE: "{t}\n" ANNOTATION: "{a}"' for t, a in zip(casino_dnd_format_examples, casino_dnd_format_annots)])
    item_counts = inst['ctx']
    reason = " ".join(inst["ctx"][inst["ctx"].index("=")+1:])
    ctx_str = f'CONTEXT: "{item_counts[0]} firewood {item_counts[2]} water {item_counts[4]} food"' + reason
    curr_utt = inst['read_inpt']

    act_prompt = [system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{curr_utt}"'])}]
    return act_prompt

def casino_cust_form_fs(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are assisting the user in annotating utterances in a negotiation for dividing 3 units each of food, water, and firewood. Respond to user requests succinctly, giving only the annotation, without extra words. Possible annotations are: "Empathy/Coordination", "Undervalue Partner", "Non-strategic", "Small Talk", "No-need", "Vouch Fairness", "Self/Other Need", "Elicit Preferences". A single input (utterance) may have multiple correct annotations.'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n ' + ' '.join([f'UTTERANCE: "{t}\n" ANNOTATION: "{a}"' for t, a in zip(casino_cust_format_examples, casino_cust_format_multilab_annots)])
    item_counts = inst['ctx']
    reason = " ".join(inst["ctx"][inst["ctx"].index("=")+1:])
    ctx_str = f'CONTEXT: "{item_counts[0]} firewoods {item_counts[2]} water {item_counts[4]} food"' + reason
    curr_utt = inst['read_inpt']

    act_prompt = [system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{curr_utt}"'])}]
    return act_prompt


# def chat_dnd_example(inst):
#     system_msg = {
#         'role': 'system',
#         'content': f'You are assisting the user in annotating utterances in a negotiation dialogue. Respond to user requests succinctly, giving only the annotation, without extra words. Possible annotations are: {", ".join([f"{k} {utility_eg_formatter(v)}" for k, v in dnd_rb_format.items()])}, and "Unknown"'
#         }

#     splt_dia = [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]

#     return [[system_msg, {'role': 'user', 'content': f'What is the annotation for this utterance? "{u}"'}] for u in splt_dia]



# # DEMO
# def example_u2a_func(inst):
#     """
#     # Get dialogue act with parser
#     parser_prompt = self.p_prompt_func({
#         'ctx': self.ctx,
#         'dialogue': self.dialogue,
#         'read_inpt': ' '.join(inpt)
#     })

#     # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
#     # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
#     """
#     scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls."
#     annot_str = f'You are assisting the user in annotating utterances in a negotiation dialogue. Respond to user requests succinctly, giving only the annotation, without extra words. Possible annotations are: {", ".join([f"{k} {utility_eg_formatter(v)}" for k, v in dnd_rb_format.items()])}, and "Unknown"'
#     print("TEST!")
#     if len(inst['dialogue']) == 0:
#         return [f"{scenario_str}\n{annot_str}"]
#     else:
#         dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
#         return [f"{scenario_str}\n{dialogue_str}\n{annot_str}"]


# def dnd_parser_chatcomp(inst):
#     """
#     # Get dialogue act with parser
#     parser_prompt = self.p_prompt_func({
#         'ctx': self.ctx,
#         'dialogue': self.dialogue,
#         'read_inpt': ' '.join(inpt)
#     })

#     # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
#     # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
#     """
#     system_msg = {
#         'role': 'system',
#         'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue, given the context of how many of each item is available. Possible annotations are: "greet", "inquire:, "propose", "disagree", "insist", and "agree"'
#         }
#     user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'{t}\nANNOTATION: "{a}"' for t, a in zip(dnd_fs_texts, dnd_fs_annots_no_vc)])

#     ctx_str = f'CONTEXT: "{inst["ctx"][0]} books {inst["ctx"][1]} hats {inst["ctx"][2]} balls"'

#     splt_dia = [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]
#     print("TEST!")
#     print(f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{inst["read_inpt"]}"')
    
#     return [[system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{inst["read_inpt"]}"'])}]]

