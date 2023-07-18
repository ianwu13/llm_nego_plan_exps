"""
Functions which convert instances from datasethandler and corresponding annotations from llms into string (line) outputs
for raw dataset files
"""

# DEMO FUNCTIONS
def example_dia_response_func(inst):
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}. Your partner has different values for each item and you are negotiating to maximize your own points."
    if len(inst['dialogue']) == 0:
        return [f"{scenario_str}\nThe best greeting to start this negotiation is: "]
    else:
        dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
        return [f"{scenario_str}\n{dialogue_str}\nIf an agreement has been reached, say <selection>\nThe best response in this negotiation is: "]

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

def example_choice_func(inst):
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}. Your partner has different values for each item and you are negotiating to maximize your own points."
    dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
    return [f"{scenario_str}\n{dialogue_str}\nThe agreed upon values for the deal, in the format\nyour_books your_hats your_balls their_books their_hats their_balls\n (six numbers), are: "]


# DIALOGUE RESPONSE PROMPT FUNCTIONS

def dia_resp_slagent_chatcomp(inst):
    """
    openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )
    """
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    system_str = f'There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]}. Your partner has different values for each item and you are negotiating over how to divide the items. Your goal is to mazimize your own points in the agreed upon deal. When a deal is agreed upon, say "<selection>" for make a selection'
    messages = [{"role": "system", "content": system_str}]
    if len(inst['dialogue']) == 0:
        messages.append({"role": "user", "content": f"Begin the negotiation"})
        return [messages]
    else:
        # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
        you_them_dict = {
            'YOU:': 'assistant',
            'THEM:': 'user'
        }
        dia_arr = inst['dialogue']
        assert dia_arr[0] in you_them_dict, f'UNIDENTIFIED STARTING TOKEN FOUND: {dia_arr[i]}, Should be either "YOU:" or "THEM:"'
        i = 0
        while i < len(inst['dialogue']):
            role = you_them_dict[dia_arr[i]]
            i += 1
            end = i
            while end < len(inst['dialogue']) and dia_arr[end] not in you_them_dict:
                end += 1
            content = ' '.join(dia_arr[i:end])
            messages.append({"role": role, "content": content})
            i = end

        return [messages]


# CHOICE/SELECTION MAKING PROMPT FUNCTIONS

def choice_slagent_chatcomp(inst):
    system_str = f'There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls available. You are an assistant negotiating over books, hats, and balls to divide them. Your goal is to mazimize your own points. When a participant says "<selection>", this indicates a deal has been reached. In response to this, please give the agreed upon values for the deal, in the order "your_books your_hats your_balls their_books their_hats their_balls" (six numbers), without any additional words. The total number of books, hats, and balls given should equal the number available.'
    messages = [{"role": "system", "content": system_str}]
    if len(inst['dialogue']) == 0:
        messages.append({"role": "user", "content": f"Begin the negotiation"})
        return [messages]
    else:
        # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
        you_them_dict = {
            'YOU:': 'assistant',
            'THEM:': 'user'
        }
        dia_arr = inst['dialogue']
        assert dia_arr[0] in you_them_dict, f'UNIDENTIFIED STARTING TOKEN FOUND: {dia_arr[i]}, Should be either "YOU:" or "THEM:"'
        i = 0
        while i < len(inst['dialogue']):
            role = you_them_dict[dia_arr[i]]
            i += 1
            end = i
            while end < len(inst['dialogue']) and dia_arr[end] not in you_them_dict:
                end += 1
            content = ' '.join(dia_arr[i:end])
            messages.append({"role": role, "content": content})
            i = end

        return [messages]
