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

# TODO: TEST THIS ONCE OPENAI API SPEEDS UP
def dia_resp_slagent_completion_dnd(inst):
    # You is alice
    prompt_str = f'Alice and Bob are negotiating over how to divide books, hats, and balls. There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]} to Alice. Bob has different but unknown values for each item. Both Alice and Bobs goal is to mazimize their own points in the final deal. When a deal is agreed upon, the participants say "<selection>" to make a selection.'
    
    if len(inst['dialogue']) == 0:
        return prompt_str + '\nAlice: '
    else:
        # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
        sub_dict = {
            'THEM:': 'Bob:', 
            'YOU:': 'Alice:'
            }
        for w in inst['dialogue']:
            if w in sub_dict:
                prompt_str += '\n' + sub_dict[w]
                last = w
            else:
                prompt_str += ' ' + w
        if last == 'THEM:':  # This should always be true
            prompt_str += '\nAlice:'
        else:
            prompt_str += '\Bob:'

        return prompt_str

def dia_resp_slagent_chatcomp_dnd(inst):
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
    system_str = f'There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]}. Your partner has different values for each item and you are negotiating over how to divide the items. Your goal is to mazimize your own points in the agreed upon deal. To indicate that a deal has been reached, output the word "<selection>"'  #  When a deal is reached, you will output the word "<selection>" as your next response
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

# TODO: TEST THIS ONCE OPENAI API SPEEDS UP
def choice_slagent_completion_dnd(inst):
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}. Your partner has different values for each item and you are negotiating to maximize your own points."
    dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
    return [f"{scenario_str}\n{dialogue_str}\nThe agreed upon values for the deal, in the format\nyour_books your_hats your_balls their_books their_hats their_balls\n (six numbers), are: "]

    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    
    # You is alice
    prompt_str = f'Alice and Bob are negotiating over how to divide books, hats, and balls. There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]} to Alice. Bob has different but unknown values for each item and they are negotiating over how to divide the items. Both Alice and Bobs goal is to mazimize their own points in the final deal. When a deal is agreed upon, the participants say "<selection>" to make a selection.'
    
    if len(inst['dialogue']) == 0:
        return prompt_str + '\nAlice: '
    else:
        # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
        sub_dict = {
            'THEM:': 'Bob:', 
            'YOU:': 'Alice:'
            }
        for w in inst['dialogue']:
            if w in sub_dict:
                prompt_str += '\n' + sub_dict[w]
                last = w
            else:
                prompt_str += ' ' + w

        prompt_str += '\nThe agreed upon values for the deal, in the format "alice_books alice_hats alice_balls bob_books bob_hats bob_balls" (six numbers), are: '

        return prompt_str

def choice_slagent_chatcomp_dnd(inst):
    system_str = f'You are an assistant negotiating with the user over how to divide {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. When a participant says "<selection>", this indicates a deal has been reached. In response to this, give the agreed upon values for the deal, in the order "assistant_number_of_books assistant_number_of_hats assistant_number_of_balls user_number_of_books user_number_of_hats user_number_of_balls" (six numbers), without any additional words. The total number of books, hats, and balls given to you and the user should equal the number available.'
    messages = [{"role": "system", "content": system_str}]
    assert len(inst['dialogue']) > 0, 'Must have some dialogue to reach a deal'

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
    if messages[-1]['role'] == 'assistant':
        messages.append({"role": "user", "content": '<selection>'})

    return [messages]


# DIALOGUE ACT LEVEL RESPONSE PROMPT FUNCTIONS

# TODO
def dia_act_chatcomp(inst):
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
