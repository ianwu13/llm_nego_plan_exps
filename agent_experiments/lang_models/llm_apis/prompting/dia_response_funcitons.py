"""
Functions which convert instances from datasethandler and corresponding annotations from llms into string (line) outputs
for raw dataset files
"""


# DEMO
def example_dia_response_func(inst):
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}. Your partner has different values for each item and you are negotiating to maximize your own points."
    if len(inst['dialogue']) == 0:
        return [f"{scenario_str}\nThe best greeting to start this negotiation is: "]
    else:
        dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
        return [f"{scenario_str}\n{dialogue_str}\nIf an agreement has been reached, say <selection>\nThe best response in this negotiation is: "]


# DEMO
def example_dia_act_response_func(inst):
    """
    resp_da_prompt = self.rpf({
        'ctx': self.ctx,
        'dialogue': self.dialogue,
        'dia_acts': self.dialogue_acts
    })
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    """
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}. Your partner has different values for each item and you are negotiating to maximize your own points."
    if len(inst['dialogue']) == 0:
        return [f"{scenario_str}\nThe best dialogue strategy to start this negotiation is: "]
    else:
        dialogue_str = "" # f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
        # NOTE: Adding nl dialogue here leads model to respond with nl utterance even when instructed to doa  dialogue act
        da_str = f"The series of dialogue strategy acts used so far is: {' '.join(inst['dia_acts'])}"
        return [f'{scenario_str}\n{dialogue_str}\n{da_str}\nIf an agreement has been reached, say <selection>\nFollowing this template: "propose book=YOUR_BOOKS_COUNT hat=YOUR_HATS_COUNT ball=YOUR_BALLS_COUNT", the best dialogue strategy act to respond with: ']


# DEMO
def example_choice_func(inst):
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}. Your partner has different values for each item and you are negotiating to maximize your own points."
    dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
    return [f"{scenario_str}\n{dialogue_str}\nThe agreed upon values for the deal, in the format\nyour_books their_books your_hats their_hats your_balls their_balls\n (six numbers), are: "]
