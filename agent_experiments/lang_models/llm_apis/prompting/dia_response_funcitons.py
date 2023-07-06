"""
Functions which convert instances from datasethandler and corresponding annotations from llms into string (line) outputs
for raw dataset files
"""


# DEMO
def example_dia_response_func(inst):
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}"
    if len(inst['dialogue']) == 0:
        return [f"{scenario_str}\nThe best greeting to start this negotiation is: "]
    else:
        dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
        return [f"{scenario_str}\n{dialogue_str}\nIf an agreement has been reached, say <selection>\nThe best response in this negotiation is: "]


# DEMO
def example_choice_func(inst):
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}"
    dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
    return [f"{scenario_str}\n{dialogue_str}\nThe agreed upon values for the deal, in the format\nyour_books their_books your_hats their_hats your_balls their_balls\n (six numbers), are: "]
