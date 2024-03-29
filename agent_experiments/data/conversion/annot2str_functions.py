"""
Functions which convert instances from datasethandler and corresponding annotatins from llms into string (line) outputs
for raw dataset files
"""

from data.casino import POINTS_MAP, ORDER_MAP
from simple_utils import remove_prefix

# FINAL ANNOT FUNCTIONS USED: base_casino, dnd_lstrip_annotation


def base_out_formatter_dnd(inst, annot):
    input_str = ' '.join([f'{c} {v}' for c, v in zip(inst['input']['count'], inst['input']['value'])])
    prt_inpt_str = ' '.join([f'{c} {v}' for c, v in zip(inst['partner_input']['count'], inst['partner_input']['value'])])

    output = inst['output']
    tmp = output.split(' ')
    prt_output = ' '.join([tmp[3], tmp[4], tmp[5], tmp[0], tmp[1], tmp[2]])

    you_start = inst['dialogue'].startswith('YOU: ')

    dia = ''
    prt_persp_dia = ''
    for u, a in zip(inst['dialogue'].split(' <eos> '), annot):
        if '<selection>' in u:
            a = '<selection>'
        else:
            a = a.replace(', ', ' ').replace(',', ' ') + ' <eos>'

        if you_start:
            dia += ' YOU: '
            prt_persp_dia += ' THEM: '
        else:
            dia += ' THEM: '
            prt_persp_dia += ' YOU: '
        you_start = not you_start
        dia += a
        prt_persp_dia += a
    # Remove leading space
    dia = dia.lstrip(' ')
    prt_persp_dia = prt_persp_dia.lstrip(' ')

    return f'<input> {input_str} </input> <dialogue> {dia} </dialogue> <output> {output} </output> <partner_input> {prt_inpt_str} </partner_input>\n'
    # THIS IS FOR PARTNER BUT THAT IS INCLUDED IN DSET '<input> {prt_inpt_str} </input> <dialogue> {prt_persp_dia} </dialogue> <output> {prt_output} </output> <partner_input> {input_str} </partner_input>\n'


def base_out_formatter_casino(inst, annot):
    # prtnr is mturk_agent_2, you are mturk_agent_1
    tmp = [None, None, None]
    for k, v in inst['participant_info']['mturk_agent_1']['value2issue'].items():
        tmp[ORDER_MAP[v]] = POINTS_MAP[k]
    input_str = ' '.join([f'3 {pts_val}' for pts_val in tmp])
    tmp = [None, None, None]
    for k, v in inst['participant_info']['mturk_agent_2']['value2issue'].items():
        tmp[ORDER_MAP[v]] = POINTS_MAP[k]
    prt_inpt_str = ' '.join([f'3 {pts_val}' for pts_val in tmp])

    if inst['chat_logs'][-2]['text'] == "Submit-Deal" and inst['chat_logs'][-1]['text'] == "Accept-Deal":
        # These give wrong order output
        # output_a = ' '.join(f'{k}={int(v)}' for k, v in inst['chat_logs'][-2]['task_data']['issue2youget'].items())
        # output_b = ' '.join(f'{k}={int(v)}' for k, v in inst['chat_logs'][-2]['task_data']['issue2theyget'].items())

        yg = inst['chat_logs'][-2]['task_data']['issue2youget']
        tg = inst['chat_logs'][-2]['task_data']['issue2theyget']

        output_a = f"item0={yg['Food']} item1={yg['Water']} item2={yg['Firewood']}"
        output_b = f"item0={tg['Food']} item1={tg['Water']} item2={tg['Firewood']}"

        if inst['chat_logs'][-2]['id'] == 'mturk_agent_1':
            output = output_a + ' ' + output_b
            if inst['chat_logs'][-1]['text'] == "Accept-Deal":
                prt_output = output_b + ' ' + output_a
            else:
                prt_output = '<no_agreement> <no_agreement> <no_agreement> <no_agreement> <no_agreement> <no_agreement>'
        else:
            prt_output = output_a + ' ' + output_b
            if inst['chat_logs'][-1]['text'] == "Accept-Deal":
                output = output_b + ' ' + output_a
            else:
                output = '<no_agreement> <no_agreement> <no_agreement> <no_agreement> <no_agreement> <no_agreement>'
        
        inst['chat_logs'] = inst['chat_logs'][:-1]
        inst['chat_logs'][-1]['text'] = "Accept-Deal"
    else:
        output = '<no_agreement> <no_agreement> <no_agreement> <no_agreement> <no_agreement> <no_agreement>'
        prt_output = '<no_agreement> <no_agreement> <no_agreement> <no_agreement> <no_agreement> <no_agreement>'

    you_start = inst['chat_logs'][0]['id'] == 'mturk_agent_1'
    dia = ''
    prt_persp_dia = ''
    for i, a in zip(inst['chat_logs'], annot):
        if i['text'] == 'Accept-Deal':
            a = '<selection>'
        elif i['text'] == 'Submit-Deal':
            a = 'agree'
        elif i['text'] == 'Reject-Deal':
            a = 'disagree'
        elif i['text'] == 'Walk-Away':
            a = 'disagree'
        else:
            a = a.replace(', ', ' ').replace(',', ' ') + ' <eos>'

        if you_start:
            dia += ' YOU: '
            prt_persp_dia += ' THEM: '
        else:
            dia += ' THEM: '
            prt_persp_dia += ' YOU: '
        you_start = not you_start
        dia += a
        prt_persp_dia += a
    # Remove leading space
    dia = dia.lstrip(' ')
    prt_persp_dia = prt_persp_dia.lstrip(' ')

    if not dia.endswith(' <selection>'):
        dia += ' <selection>'
    if not prt_persp_dia.endswith(' <selection>'):
        prt_persp_dia += ' <selection>'

    # Handle eos at end if necessary
    
    return f'<input> {input_str} </input> <dialogue> {dia} </dialogue> <output> {output} </output> <partner_input> {prt_inpt_str} </partner_input>\n<input> {prt_inpt_str} </input> <dialogue> {prt_persp_dia} </dialogue> <output> {prt_output} </output> <partner_input> {input_str} </partner_input>\n'


# Removes content after "\n" character in LLM output
def base_out_formatter_first_line_dnd(inst, annot):
    return base_out_formatter_dnd(inst, [a.split('\n')[0] for a in annot])


def base_out_formatter_first_line_casino(inst, annot):
    return base_out_formatter_casino(inst, [a.split('\n')[0] for a in annot])


def dnd_lstrip_annotation(inst, annot):
    annot = [remove_prefix(remove_prefix(a.split('\n')[0], 'annotation'), 'the annotation for this utterance is ').lstrip(' ') for a in annot]
    
    input_str = ' '.join([f'{c} {v}' for c, v in zip(inst['input']['count'], inst['input']['value'])])
    prt_inpt_str = ' '.join([f'{c} {v}' for c, v in zip(inst['partner_input']['count'], inst['partner_input']['value'])])

    output = inst['output']
    tmp = output.split(' ')
    prt_output = ' '.join([tmp[3], tmp[4], tmp[5], tmp[0], tmp[1], tmp[2]])

    you_start = inst['dialogue'].startswith('YOU: ')

    dia = ''
    prt_persp_dia = ''
    for u, a in zip(inst['dialogue'].split(' <eos> '), annot):
        if '<selection>' in u:
            a = '<selection>'
        else:
            a = a.replace(', ', ' ').replace(',', ' ') + ' <eos>'

        if you_start:
            dia += ' YOU: '
            prt_persp_dia += ' THEM: '
        else:
            dia += ' THEM: '
            prt_persp_dia += ' YOU: '
        you_start = not you_start
        dia += a
        prt_persp_dia += a
    # Remove leading space
    dia = dia.lstrip(' ')
    prt_persp_dia = prt_persp_dia.lstrip(' ')

    return f'<input> {input_str} </input> <dialogue> {dia} </dialogue> <output> {output} </output> <partner_input> {prt_inpt_str} </partner_input>\n'


# DEMO STUFF
def example_annot2s_func(inst, annot):
    # Just for casino dataset, returns generic string with preferences and annotations for each agent perspective
    a1_pref_str = ' '.join([f'{p}: {i}' for p, i in inst['participant_info']['mturk_agent_1']['value2issue'].items()])
    a2_pref_str = ' '.join([f'{p}: {i}' for p, i in inst['participant_info']['mturk_agent_2']['value2issue'].items()])
    annots_str = ''.join(['<eos>'.join(annot), '\n'])

    return ''.join([a1_pref_str, ' ', annots_str, a2_pref_str, ' ', annots_str])


# split utterance seperately for dnd
def utters_split_seperate(line):
    # without the final selection
    utters_list = []
    for i in range (0, len(line.split("<eos>"))):
        each = line.split("<eos>")[i]
        utters_list.append(each)
    return utters_list


def pair_utter_annot(utter_list, annot_list):
    result_list = []
    # Pair utterances with annotations
    for i in range(0, len(utter_list)):
        each_str = utter_list[i] + " " + annot_list[i]
        result_list.append(each_str)

    # Append all utterances with annotation to one line
    result_str = ''
    for each in result_list:
        result_str = result_str + " " + each
    return result_str


def demo_dnd_outform(inst, annot):
    dialogue_str = inst['dialogue']
    utterance_list = utters_split_seperate(dialogue_str)
    return pair_utter_annot(utterance_list, annot)


def demo_casino_outform(inst, annot):
    # inst is a dict

    # Extract utterances from instances
    utterance_list = []
    for each in inst['chat_logs']:
        uttr = f"{each['id']}: {each['text']}"
        utterance_list.append(uttr)

    return pair_utter_annot(utterance_list, annot)
