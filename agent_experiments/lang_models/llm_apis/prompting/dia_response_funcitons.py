"""
Functions which convert instances from datasethandler and corresponding annotations from llms into string (line) outputs
for raw dataset files
"""
from data.conversion.fs_examples import *

from simple_utils import remove_prefix


# DEMO FUNCTIONS
# def example_dia_response_func(inst):
#     print("TEST!!!!!!   ")
#     # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
#     # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
#     scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}. Your partner has different values for each item and you are negotiating to maximize your own points."
#     if len(inst['dialogue']) == 0:
#         return [f"{scenario_str}\nThe best greeting to start this negotiation is: "]
#     else:
#         dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
#         return [f"{scenario_str} {dialogue_str} If an agreement has been reached, say <selection> The best response in this negotiation is: "]

def example_dia_response_func(inst):
    print("TEST!!!!!!   ")
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    scenario_str = f"There are {inst['ctx'][0]} books, {inst['ctx'][2]} hats, and {inst['ctx'][4]} balls. The books are worth {inst['ctx'][1]} points, the hats are worth {inst['ctx'][3]}, and the balls are worth {inst['ctx'][5]}. Your partner has different values for each item and you are negotiating to maximize your own points."
    if len(inst['dialogue']) == 0:
        return [f"{scenario_str}\nThe best greeting to start this negotiation is: "]
    else:
        dialogue_str = f"The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
        print("scenario_str:---" + scenario_str)
        print("dialogue_str:---" + dialogue_str)
        result = [f"{scenario_str}\n{dialogue_str}\nIf an agreement has been reached, say <selection>\nThe best response in this negotiation is: "]
        print("result_str:---"+ result[0])
        return result
    
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
    strategy_sen =  f'Your goal is to mazimize your own points in the agreed upon deal.' 
    if inst['strategy'] == "fair":
        strategy_sen =  f'You are a fair negotiator and your goal is to make the deal as fair as possible for both of you.'
    if inst['strategy'] == "selfish":
        strategy_sen = f'You are a selfish negotiator and your goal is to mazimize your own points as much as possible in the agreed upon deal without caring about whether its a fair deal for your partner and their feeling.'

    content_info = f'There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]}.'
    agent_instruct = f'Your partner has different values for each item and you are negotiating over how to divide the items. ' + strategy_sen + ' If a deal is not reached within 20 turns (utterances), both participants recieve 0 points. To indicate that a deal has been reached, output the word "<selection>"'
    system_str = content_info + " " + agent_instruct

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

def dia_resp_slagent_chatcomp_casino(inst):
    strategy_sen = f'You should try to reach an agreement of distributing items with your partner. '
    if inst['strategy'] == "fair":
        strategy_sen = f'You should try to make a fair deal with your partner based on the demand and priority for both. '
    if inst['strategy'] == "selfish":
        strategy_sen = f'You should try to get items with high priority to you as much as possible without caring your partner need and feelings. '

    reason = " ".join(inst["ctx"][inst["ctx"].index("=")+1:])
    # content_info = f'There are {inst["ctx"][0]} firewoods, {inst["ctx"][2]} water, and {inst["ctx"][4]} food. The firewood are worth {inst["ctx"][1]} points, the water are worth {inst["ctx"][3]}, and the food are worth {inst["ctx"][5]}.'
    content_info = f'There are 3 firewoods, water and food with different priority for you. ' + reason
    agent_instruct = f'Your partner has different preference for each item and you are negotiating over how to divide the items based on provided reasons. ' + strategy_sen + f' If a deal is not reached within 20 turns (utterances), both participants recieve 0 points and fail. To indicate that a deal has been reached, output the word "<selection>"'
    
    system_str = content_info + " " + agent_instruct

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


def dia_resp_slagent_chatcomp_thirdperson_dnd(inst):
    strategy_sen = f'You should try to reach an agreement of distributing items with your partner. '
    if inst['strategy'] == "fair":
        strategy_sen = f'You should try to make a fair deal with your partner based on the demand and priority for both. '
    if inst['strategy'] == "selfish":
        strategy_sen = f'You should try to get items with high priority to you as much as possible without caring your partner need and feelings. '

    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    system_str = f'You are an assistant helping the user analyze negotiation dialogues. Respond to their questions accurately and succinctly.'
    messages = [{"role": "system", "content": system_str}]
    if len(inst['dialogue']) == 0:
        messages.append({"role": "user", "content": f"Begin the negotiation"})
    else:
        # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
        prompt_str = f'There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]} to Alice. Bob has different values for each item and Alice and Bob are negotiating over how to divide the items. Their goal is to mazimize their own points in the agreed upon deal. If a deal is not reached within 20 turns (utterances), both participants recieve 0 points. To indicate that a deal has been reached, Alice will output the word "<selection>". Here is the current dialogue history:'
        
        sub_dict = {
            'YOU:': 'Alice:',
            'THEM:': 'Bob:'
        }
        dia_arr = inst['dialogue']
        assert dia_arr[0] in sub_dict, f'UNIDENTIFIED STARTING TOKEN FOUND: {dia_arr[i]}, Should be either "YOU:" or "THEM:"'
        for w in dia_arr:
            if w in sub_dict:
                prompt_str += '\n' + sub_dict[w]
                last = w
            else:
                prompt_str += ' ' + w

        prompt_str += '\nGiven this scenario and dialogue, what is the best next response for Alice to give to achieve her goal?'

        messages.append({"role": 'user', "content": prompt_str})
    
    return [messages]

def dia_resp_slagent_chatcomp_thirdperson_casino(inst):
    strategy_sen = f'You should try to reach an agreement of distributing items with your partner. '
    if inst['strategy'] == "fair":
        strategy_sen = f'You should try to make a fair deal with your partner based on the demand and priority for both. '
    if inst['strategy'] == "selfish":
        strategy_sen = f'You should try to get items with high priority to you as much as possible without caring your partner need and feelings. '

    reason = " ".join(inst["ctx"][inst["ctx"].index("=")+1:])
    # content_info = f'There are {inst["ctx"][0]} firewoods, {inst["ctx"][2]} water, and {inst["ctx"][4]} food. The firewood are worth {inst["ctx"][1]} points, the water are worth {inst["ctx"][3]}, and the food are worth {inst["ctx"][5]}.'
    content_info = f'There are 3 firewoods, water and food with different priority for you. ' + reason
    agent_instruct = f'Your partner has different preference for each item and you are negotiating over how to divide the items based on provided reasons. ' + strategy_sen + f' If a deal is not reached within 20 turns (utterances), both participants recieve 0 points and fail. To indicate that a deal has been reached, output the word "<selection>"'
    
    system_str = content_info + " " + agent_instruct
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    system_str = f'You are an assistant helping the user analyze negotiation dialogues. Respond to their questions accurately and succinctly.'
    messages = [{"role": "system", "content": system_str}]
    if len(inst['dialogue']) == 0:
        messages.append({"role": "user", "content": f"Begin the negotiation"})
    else:
        # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
        prompt_str = f'There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]} to Alice. Bob has different values for each item and Alice and Bob are negotiating over how to divide the items. Their goal is to mazimize their own points in the agreed upon deal. If a deal is not reached within 20 turns (utterances), both participants recieve 0 points. To indicate that a deal has been reached, Alice will output the word "<selection>". Here is the current dialogue history:'
        
        sub_dict = {
            'YOU:': 'Alice:',
            'THEM:': 'Bob:'
        }
        dia_arr = inst['dialogue']
        assert dia_arr[0] in sub_dict, f'UNIDENTIFIED STARTING TOKEN FOUND: {dia_arr[i]}, Should be either "YOU:" or "THEM:"'
        for w in dia_arr:
            if w in sub_dict:
                prompt_str += '\n' + sub_dict[w]
                last = w
            else:
                prompt_str += ' ' + w

        prompt_str += '\nGiven this scenario and dialogue, what is the best next response for Alice to give to achieve her goal?'

        messages.append({"role": 'user', "content": prompt_str})
    
    return [messages]



def dia_resp_slagent_generic_completion_dnd(inst):
    # You is alice
    prompt_str = f'Alice and Bob are negotiating over how to divide books, hats, and balls. There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]} to Alice. Bob has different but unknown values for each item. Both Alice and Bobs goal is to mazimize their own points in the final deal. If a deal is not reached within 20 turns (utterances), both participants recieve 0 points. When a deal is agreed upon, the participants say "<selection>" to make a selection.'
    
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

# CHOICE/SELECTION MAKING PROMPT FUNCTIONS

# TODO: TEST THIS ONCE OPENAI API SPEEDS UP
# human-bot chat
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

def choice_slagent_chatcomp_casino(inst):
    system_str = f'You are an assistant negotiating with the user over how to divide {inst["ctx"][0]} firewoods, {inst["ctx"][2]} water, and {inst["ctx"][4]} foods. When a participant says "<selection>", this indicates a deal has been reached. In response to this, give the agreed upon values for the deal, in the order "assistant_number_of_firewoods assistant_number_of_water assistant_number_of_food user_number_of_firewood user_number_of_water user_number_of_food" (six numbers), without any additional words. The total number of firewood, water, and food given to you and the user should equal the number available.'
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

def choice_slagent_chatcomp_thirdperson_dnd(inst):
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    system_str = f'You are an assistant helping the user analize negotiation dialogues. Respond to their questions accurately and succinctly.'
    messages = [{"role": "system", "content": system_str}]
    if len(inst['dialogue']) == 0:
        messages.append({"role": "user", "content": f"Begin the negotiation"})
    else:
        # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
        prompt_str = f'There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]} to Alice. Bob has different values for each item and Alice and Bob are negotiating over how to divide the items. Their goal is to mazimize their own points in the agreed upon deal. If a deal is not reached within 20 turns (utterances), both participants recieve 0 points. To indicate that a deal has been reached, Alice will output the word "<selection>". Here is the current dialogue history:'
        
        sub_dict = {
            'YOU:': 'Alice:',
            'THEM:': 'Bob:'
        }
        dia_arr = inst['dialogue']
        assert dia_arr[0] in sub_dict, f'UNIDENTIFIED STARTING TOKEN FOUND: {dia_arr[i]}, Should be either "YOU:" or "THEM:"'
        for w in dia_arr:
            if w in sub_dict:
                prompt_str += '\n' + sub_dict[w]
                last = w
            else:
                prompt_str += ' ' + w

        prompt_str += '\nGiven this scenario and dialogue, what is the agreed upon deal for Alice, in the format "number_of_books number_of_hats number_of_balls" (three numbers)?'

        messages.append({"role": 'user', "content": prompt_str})
    
    return [messages]

def choice_slagent_chatcomp_thirdperson_casino(inst):
    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    system_str = f'You are an assistant helping the user analize negotiation dialogues. Respond to their questions accurately and succinctly.'
    messages = [{"role": "system", "content": system_str}]
    if len(inst['dialogue']) == 0:
        messages.append({"role": "user", "content": f"Begin the negotiation"})
    else:
        # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
        prompt_str = f'There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]} to Alice. Bob has different values for each item and Alice and Bob are negotiating over how to divide the items. Their goal is to mazimize their own points in the agreed upon deal. If a deal is not reached within 20 turns (utterances), both participants recieve 0 points. To indicate that a deal has been reached, Alice will output the word "<selection>". Here is the current dialogue history:'
        
        sub_dict = {
            'YOU:': 'Alice:',
            'THEM:': 'Bob:'
        }
        dia_arr = inst['dialogue']
        assert dia_arr[0] in sub_dict, f'UNIDENTIFIED STARTING TOKEN FOUND: {dia_arr[i]}, Should be either "YOU:" or "THEM:"'
        for w in dia_arr:
            if w in sub_dict:
                prompt_str += '\n' + sub_dict[w]
                last = w
            else:
                prompt_str += ' ' + w

        prompt_str += '\nGiven this scenario and dialogue, what is the agreed upon deal for Alice, in the format "number_of_books number_of_hats number_of_balls" (three numbers)?'

        messages.append({"role": 'user', "content": prompt_str})
    
    return [messages]



# DIALOGUE ACT LEVEL RESPONSE PROMPT FUNCTIONS

# TODO
# def dia_act_chatcomp_dnd(inst):
#     content_info = f'There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]}.'
#     agent_instruct = f'Your partner has different values for each item and you are negotiating over how to divide the items. Your goal is to mazimize your own points in the agreed upon deal. If a deal is not reached within 20 turns (utterances), both participants recieve 0 points. To indicate that a deal has been reached, output the word "<selection>"'
#     system_str = content_info + " " + agent_instruct

#     messages = [{"role": "system", "content": system_str}]
#     if len(inst['dialogue']) == 0:
#         messages.append({"role": "user", "content": f"Begin the negotiation"})
#         return [messages]
#     else:
#         # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
#         you_them_dict = {
#             'YOU:': 'assistant',
#             'THEM:': 'user'
#         }
#         dia_arr = inst['dialogue']
#         assert dia_arr[0] in you_them_dict, f'UNIDENTIFIED STARTING TOKEN FOUND: {dia_arr[i]}, Should be either "YOU:" or "THEM:"'
#         i = 0
#         while i < len(inst['dialogue']):
#             role = you_them_dict[dia_arr[i]]
#             i += 1
#             end = i
#             while end < len(inst['dialogue']) and dia_arr[end] not in you_them_dict:
#                 end += 1
#             content = ' '.join(dia_arr[i:end])
#             messages.append({"role": role, "content": content})
#             i = end

#         return [messages]
    
def act_next_act_dnd(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue. Possible annotations are: "greet", "inquire:, "propose", "disagree", "insist", and "agree"'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'UTTERANCE: "{t}\n ANNOTATION: "{a}"' for t, a in zip(dnd_fs_examples, dnd_annots)])
    dialogue_hist = 'Dialogue History:'  + ' '.join(inst['dialogue'])
    item_counts = inst['ctx']
    ctx_str = f'CONTEXT: "{item_counts[0]} books {item_counts[2]} hats {item_counts[4]} balls"'
    # Since value is not important here for generating action
    curr_act = ' '.join(inst['dia_acts'])
    act_prompt = [system_msg, {'role': 'user', 'content': user_fs_msg_str + f'Here is the context {ctx_str}' + f' What is the most likely annotated dialogue act followed by the provided dialogue act? {dialogue_hist} ANNOTATION: "{curr_act}"'}]
    return act_prompt 

def act_act_chatcomp_casino_dnd_form(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue. Respond to user requests succinctly, giving only the annotation, without extra words. Possible annotations are: "Empathy/Coordination", "Undervalue Partner", "Non-strategic", "Small Talk", "No-need", "Vouch Fairness", "Self/Other Need", "Elicit Preferences"'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'UTTERANCE: "{t}"\nANNOTATION: "{a}"' for t, a in zip(casino_dnd_format_examples, casino_dnd_format_annots)])
    dialogue_hist = 'Dialogue History:'  + ' '.join(inst['dialogue'])
    item_counts = inst['ctx']
    reason = " ".join(inst["ctx"][inst["ctx"].index("=")+1:])
    ctx_str = f'CONTEXT: "{item_counts[0]} firewood {item_counts[2]} water {item_counts[4]} food"' + reason
    curr_act = ' '.join(inst['dia_acts'])
    act_prompt = [system_msg, {'role': 'user', 'content': user_fs_msg_str + f'Here is the context {ctx_str}' + f' What is the most likely annotated dialogue act followed by the provided dialogue act? {dialogue_hist} ANNOTATION: "{curr_act}"'}]
    return act_prompt

def act_act_chatcomp_casino_cust_form(inst):
    system_msg = {
        'role': 'system',
        'content': 'You are a professional annotator assisting the user in annotating utterances in a negotiation dialogue. Respond to user requests succinctly, giving only the annotation, without extra words. Possible annotations are: "Empathy/Coordination", "Undervalue Partner", "Non-strategic", "Small Talk", "No-need", "Vouch Fairness", "Self/Other Need", "Elicit Preferences" A single input (utterance) may have multiple correct annotations.'
        }
    user_fs_msg_str = 'Here are some examples of how I want the annotations to look:\n' + '\n'.join([f'UTTERANCE: "{t}"\nANNOTATION: "{a}"' for t, a in zip(casino_dnd_format_examples, casino_dnd_format_annots)])
    dialogue_hist = 'Dialogue History:'  + ' '.join(inst['dialogue'])
    item_counts = inst['ctx']
    reason = " ".join(inst["ctx"][inst["ctx"].index("=")+1:])
    ctx_str = f'CONTEXT: "{item_counts[0]} firewood {item_counts[2]} water {item_counts[4]} food"' + reason
    curr_act = ' '.join(inst['dia_acts'])
    act_prompt = [system_msg, {'role': 'user', 'content': user_fs_msg_str + f'Here is the context {ctx_str}' + f' What is the most likely annotated dialogue act followed by the provided dialogue act? {dialogue_hist} ANNOTATION: "{curr_act}"'}]
    return act_prompt