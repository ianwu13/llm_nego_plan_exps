"""
Functions which convert instances from datasethandler and corresponding annotatins from llms into string (line) outputs
for raw dataset files
"""


def base_out_formatter(inst, annot):
    pass


# Removes content after "\n" character in LLM output
def base_out_formatter_first_line():
    pass


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
