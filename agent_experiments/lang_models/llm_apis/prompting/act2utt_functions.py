"""
Functions which convert instances from datasethandler and corresponding annotatins from llms into string (line) outputs
for raw dataset files
"""


# DEMO
def example_a2u_func(inst):
    """
    generator_prompt = self.g_prompt_func({
        'ctx': self.ctx,
        'dialogue': self.dialogue,
        'dia_acts': self.dialogue_acts,
        'gen_act': resp_da
    })

    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    """
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}. Your partner has different values for each item and you are negotiating to maximize your own points."
    if len(inst['dialogue']) == 0:
        gen_act_str = f"The annotated dialogue act for your first response is: {' '.join(inst['gen_act'])}\n the corresponding natural language utterance is: "
        return [f"{scenario_str}\n{gen_act_str}"]
    else:
        dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
        da_str = f"The dialogue act annotations up to this point are: {' '.join(inst['dia_acts'])}"
        gen_act_str = f"The annotated dialogue act for your next response is: {' '.join(inst['gen_act'])}\n the corresponding natural language utterance is: "
        return [f"{scenario_str}\n{dialogue_str}\n{da_str}\n{gen_act_str}"]
