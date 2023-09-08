"""
Functions which convert instances from datasethandler and corresponding annotatins from llms into string (line) outputs
for raw dataset files
"""


# DEMO

def dnd_a2u_prompt(inst):

    """
    generator_prompt = self.g_prompt_func({
        'ctx': self.ctx,
        'strategy':self.strategy,
        'dialogue': self.dialogue,
        'dia_acts': self.dialogue_acts,
        'gen_act': resp_da
    })

    # print(inst['ctx']) -> ['1', '0', '1', '1', '3', '3']
    # print(inst['dialogue']) -> ['THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY', 'YOU:', 'DUMMY', 'THEM:', 'DUMMY']
    """
    strategy_sen =  f'Your goal is to maximize your own points in the agreed upon deal.' 
    if inst['strategy'] == "fair":
        strategy_sen =  f'You are a fair negotiator and your goal is to make the deal as fair as possible for both of you.'
    if inst['strategy'] == "selfish":
        strategy_sen = f'You are a selfish negotiator and your goal is to mazimize your own points as much as possible in the agreed upon deal without caring about whether its a fair deal for your partner and their feeling.'

    content_info = f'There are {inst["ctx"][0]} books, {inst["ctx"][2]} hats, and {inst["ctx"][4]} balls. The books are worth {inst["ctx"][1]} points, the hats are worth {inst["ctx"][3]}, and the balls are worth {inst["ctx"][5]}.'
    agent_instruct = f'Your partner has different values for each item and you are negotiating over how to divide the items. '+ strategy_sen + f' If a deal is not reached within 20 utterances, both participants recieve 0 points. To indicate that a deal has been reached, output the word "<selection>"'
    system_str = content_info + " " + agent_instruct

    messages = [{"role": "system", "content": system_str}]

    if len(inst['dialogue']) == 0:
        gen_act_str = f"The annotated dialogue act for your first response is: {inst['gen_act']}\n the corresponding natural language utterance is: "
        messages.append({"role": "user", "content": gen_act_str})
    else:
        dialogue_str = f" The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
        da_str = f" The dialogue act annotations up to this point are: {' '.join(inst['dia_acts'])}"
        gen_act_str = f" The annotated dialogue act for your next response is: {inst['gen_act']}\n If an agreement has been reached, say <selection>\n the corresponding natural language utterance is: "
        messages.append({"role": "user", "content": dialogue_str + da_str + gen_act_str})
    return messages

def casino_a2u_prompt(inst):
    strategy_sen = f'You should try to reach an agreement of distributing items with your partner. '
    if inst['strategy'] == "fair":
        strategy_sen = f'You should try to make a fair deal with your partner based on the demand and priority for both. '
    if inst['strategy'] == "selfish":
        strategy_sen = f'You should try to get items with high priority to you as much as possible without caring your partner need and feelings. '

    reason = " ".join(inst["ctx"][inst["ctx"].index("=")+1:])
    # content_info = f'There are {inst["ctx"][0]} firewoods, {inst["ctx"][2]} water, and {inst["ctx"][4]} food. The firewood are worth {inst["ctx"][1]} points, the water are worth {inst["ctx"][3]}, and the food are worth {inst["ctx"][5]}.'
    content_info = f'There are 3 firewoods, water and food with different priority for you. ' + reason
    agent_instruct = f'Your partner has different preference for each item and you are negotiating over how to divide the items based on provided reasons. ' + strategy_sen + f' If a deal is not reached within 20 utterances, both participants recieve 0 points and fail. To indicate that a deal has been reached, output the word "<selection>"'
    
    system_str = content_info + " " + agent_instruct

    messages = [{"role": "system", "content": system_str}]

    if len(inst['dialogue']) == 0:
        gen_act_str = f"The annotated dialogue act for your first response is: {inst['gen_act']}\n the corresponding natural language utterance is: "
        messages.append({"role": "user", "content": gen_act_str})
    else:
        dialogue_str = f" The negotiation dialogue up to this point is: {' '.join(inst['dialogue'])}"
        da_str = f" The dialogue act annotations up to this point are: {' '.join(inst['dia_acts'])}"
        gen_act_str = f" The annotated dialogue act for your next response is: {inst['gen_act']}\n If an agreement has been reached, say <selection>\n the corresponding natural language utterance is: "
        messages.append({"role": "user", "content": dialogue_str + da_str + gen_act_str})
    return messages

# TODO
def dnd_generator_chatcomp(inst):
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
        gen_act_str = f"The annotated dialogue act for your next response is: {' '.join(inst['gen_act'])}\nIf an agreement has been reached, say <selection>\n the corresponding natural language utterance is: "
        return [f"{scenario_str}\n{dialogue_str}\n{da_str}\n{gen_act_str}"]
