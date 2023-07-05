"""
Functions which convert instances from datasethandler and corresponding annotatins from llms into string (line) outputs
for raw dataset files
"""


def example_annot2s_func(inst, annot):
    # Just for casino dataset, returns generic string with preferences and annotations for each agent perspective
    a1_pref_str = ' '.join([f'{p}: {i}' for p, i in inst['participant_info']['mturk_agent_1']['value2issue'].items()])
    a2_pref_str = ' '.join([f'{p}: {i}' for p, i in inst['participant_info']['mturk_agent_2']['value2issue'].items()])
    annots_str = ''.join(['<eos>'.join(annot), '\n'])

    return ''.join([a1_pref_str, ' ', annots_str, a2_pref_str, ' ', annots_str])


def demo_dnd_outform(inst, annot):
    pass


def demo_casino_outform(inst, annot):
    pass
