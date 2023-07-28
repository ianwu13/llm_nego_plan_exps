"""
Functions which convert instances from datasethandler and corresponding annotatins from llms into string (line) outputs
for raw dataset files
"""

from data.conversion.fs_examples import *


# DEMO
def example_u2a_func(inst):
    """
    # Get dialogue act with parser
    parser_prompt = self.p_prompt_func({
        'ctx': self.ctx,
        'dialogue': self.dialogue,
        'read_inpt': ' '.join(inpt)
    })

    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    """
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}. Your partner has different values for each item and you are negotiating to maximize your own points."
    annot_str = f'This is the most recent utterance: *{inst["read_inpt"]}*\nBased on this dialogue act template: "propose book=YOUR_BOOKS_COUNT hat=YOUR_HATS_COUNT ball=YOUR_BALLS_COUNT", This would give the dialogue act: '
    if len(inst['dialogue']) == 0:
        return [f"{scenario_str}\n{annot_str}"]
    else:
        dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
        return [f"{scenario_str}\n{dialogue_str}\n{annot_str}"]


def dnd_parser_chatcomp(inst):
    """
    # Get dialogue act with parser
    parser_prompt = self.p_prompt_func({
        'ctx': self.ctx,
        'dialogue': self.dialogue,
        'read_inpt': ' '.join(inpt)
    })

    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    """
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue, given the context of how many of each item is available. Possible annotations are: "greet", "inquire:, "propose", "disagree", "insist", and "agree"'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'{t}\nANNOTATION: "{a}"' for t, a in zip(dnd_fs_texts, dnd_fs_annots_no_vc)])

    ctx_str = f'CONTEXT: "{inst["ctx"][0]} books {inst["ctx"][1]} hats {inst["ctx"][2]} balls"'

    splt_dia = [remove_prefix(remove_prefix(u, 'YOU: '), 'THEM: ') for u in inst['dialogue'].split(' <eos> ')]

    print(f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{inst["read_inpt"]}"')
    
    return [[system_msg, {'role': 'user', 'content': '\n'.join([user_fs_msg_str, f'What is the annotation for this utterance? {ctx_str} UTTERANCE: "{inst["read_inpt"]}"'])}]]

