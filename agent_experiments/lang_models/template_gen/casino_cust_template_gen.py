import random

from lang_models.template_gen.template_utils import parse_acts, seperate_slots_w_values


CASINO_ITEMS = ['food', 'water', 'firewood']
CUST_LABELS = [
    'smalltalk',
    'empathycoordination',
    'noneed',  # NEED SLOTS
    'elicitpreference',
    'undervalue',  # NEED SLOTS
    'vouchfairness',
    'expresspreference',  # NEED SLOTS
    'propose',  # NEED SLOTS
    'disagree',
    'agree',
    'unknown',
]

def tgen_smalltalk(slots_list: list):
    return random.choice([
        "Hello!", 
        "Hey!", 
        "Hi!", 
        "How are you?", 
        "Hi, how are you?",
        "Hi, are you excited to go camping?"])

def tgen_empathycoordination(slots_list: list):
    return random.choice([
        "Do you have any good ideas about how to distribute these items?",
        "What do you think is the best way to allocate these items?",
        "Let's work together to find a good deal.", 
        "Let's try to make a deal that benefits us both!", 
        "Maybe we can split the items somehow?", 
        "I am willing to share everything.", 
        "I think we can make a fair deal here where we both will be happy.",
        "What do you need?"])

def tgen_noneed(slots_list: list):
    if len(slots_list) == 1:
        return random.choice([
            f"No thanks, I dont need {slots_list[0]}.",
            f"We already have plenty of {slots_list[0]}.",
            f"We don't need any more {slots_list[0]}."])
    elif len(slots_list) == 2:
        return random.choice([
            f"No thanks, I dont need {slots_list[0]} or {slots_list[1]}.",
            f"We already have plenty of {slots_list[0]} and {slots_list[1]}.",
            f"We don't need any more {slots_list[0]} or {slots_list[1]}."])
    else:
        return random.choice([
            "No thanks, I dont need that.",
            "We already have plenty."])

def tgen_elicitpreference(slots_list: list):
    if len(slots_list) == 1:
        return random.choice([
            f"How much {slots_list[0]} would you like?",
            f"How much do you value {slots_list[0]}?",
            f"Do you want any {slots_list[0]}?"])
    elif len(slots_list) == 2:
        return random.choice([
            f"How much {slots_list[0]} and {slots_list[1]} would you like?",
            f"How much do you value {slots_list[0]} and {slots_list[1]}?",
            f"Do you want any {slots_list[0]} or {slots_list[1]}?"])
    else:
        return random.choice([
            "How much of each resource do you want?",
            "How much do you value each resource?",
            "What are your preferences?",
            "Which items do you prefer?"])

def tgen_undervalue(slots_list: list):
    if len(slots_list) == 1:
        return random.choice([
            f"Are you sure you need that much {slots_list[0]}?",
            f"Will you have trouble carrying all that {slots_list[0]}?"])
    elif len(slots_list) == 2:
        return random.choice([
            f"Are you sure you need that much {slots_list[0]} and {slots_list[1]}?",
            f"Will you have trouble carrying all that {slots_list[0]} and {slots_list[1]}?"])
    else:
        return random.choice([
            "Are you sure you need all that?",
            "Will you have trouble carrying all those items?"])

def tgen_vouchfairness(slots_list: list):
    return random.choice([
        "I think that is a fair deal.", 
        "That sounds like a fair deal to me.", 
        "Yes I think that sounds fair.", 
        "That's a fair deal."])

def tgen_expresspreference(slots_list: list):
    if len(slots_list) == 1:
        return random.choice([
            f"I really prefer {slots_list[0]}.",
            f"I want {slots_list[0]}.",
            f"{slots_list[0]} is important for me."])
    elif len(slots_list) == 2:
        return random.choice([
            f"I really prefer {slots_list[0]} and {slots_list[1]}.",
            f"I want {slots_list[0]} and {slots_list[1]}.",
            f"{slots_list[0]} and {slots_list[1]} are important for me."])
    else:
        return "" # This should not happen, expressing preference for all items or none is not meaningful
        # random.choice([
        #     "I don't have a strong preference.",
        #     "I'd rather not share my preferences."])

def tgen_propose(slots_list: list):
    if not slots_list:  # slots_list is empty (This should not happen)
        return ""
        
    s_vals, s_no_vals = seperate_slots_w_values(slots_list)
    if s_vals:  # Will ignore s_no_vals in this case
        if len(s_vals) == 1:
            proposal_counts_str = f'{s_vals[0][1]} {s_vals[0][0]}'
        else:
            proposal_counts_str = ', and'.join([', '.join(s_vals[:-1]), s_vals[-1]])
        return random.choice([
            f"How about I get {proposal_counts_str}.",
            f"I propose that I take {proposal_counts_str}."])
    elif s_no_vals:
        if len(s_no_vals) == 1:
            proposal_counts_str = s_no_vals[0]
        else:
            proposal_counts_str = ', and'.join([', '.join(s_no_vals[:-1]), s_no_vals[-1]])
        return random.choice([
            f"How about I get some of the {proposal_counts_str}.",
            f"I propose that I take some of the {proposal_counts_str}."])

    return ""  # Should not reach here

def tgen_disagree(slots_list: list):
    return random.choice([
        "Sorry, that doesn't work for me.",
        "No, I can not accept that.",
        "That is not gonna work for me.",
        "Sorry, no.",
        "Not gonna happen."])

def tgen_agree(slots_list: list):
    return random.choice([
        "Okay.",
        "That sounds like a deal.",
        "Sounds good.",
        "Sounds great!",
        "Great.",
        "Deal.",
        # "I agree with it",
        "That works for me"])

def tgen_unknown(slots_list: list):
    return random.choice([
        "Let's negotiate some more.",
        "Hmm, I'm not sure."])
 
casino_template_index = {
    'smalltalk': tgen_smalltalk,
    'empathycoordination': tgen_empathycoordination,
    'noneed': tgen_noneed,  # NEED SLOTS
    'elicitpreference': tgen_elicitpreference,
    'undervalue': tgen_undervalue,  # NEED SLOTS
    'vouchfairness': tgen_vouchfairness,
    'expresspreference': tgen_expresspreference,  # NEED SLOTS
    'propose': tgen_propose,  # NEED SLOTS
    'disagree': tgen_disagree,
    'agree': tgen_agree,
    'unknown': tgen_unknown,
}

# prompts to rephrase all dialogue acts together at once
def gen_rephrase_prompt(da_toks: list, dialogue: list)-> list:
    acts_list = parse_acts(da_toks, CUST_LABELS, CASINO_ITEMS)
    template_gens = [casino_template_index[act[0]](act[1]) for act in acts_list]
    full_template_gen = ' '.join(template_gens)
    print('\t'+str(da_toks))
    print('\t'+full_template_gen)
    usr_prompt = f'Dialogue history:\n"{" ".join(dialogue)}"\n\nRephrase and improve this sentence to respond to fit the dialogue history:\n"{full_template_gen}"'

    messages = [
        {"role": "system", "content": "You are a helping the user in rephrasing simple sentences to be more expressive in the contet of negotiation. Rephrase the sentences to be fluid, expressive, and concise."},
        {"role": "user", "content": usr_prompt}
    ]
    return messages


# NOT IMPLEMENTING FOR NOW
# # generate one prompt for one dialogue act
# # for casino we might need reasoning?
# def gen_rephrase_alone_prompts(da_str: str, count:str = "food=1 water=2 firewood=0", reasons:str = " "):

#     system_sen =  f'Return the rephrased statement used in negotiation scenario.' 
#     messages = [{"role": "system", "content": system_sen }]

#     # get a random template response for a dialogue action
#     template_response = get_temp(da_str)

#     extra_info = ""
#     # TODO: add more info based on different dialogue act
#     if da_str == "express preference":
#         extra_info = ""
#         # add extra_info with the parsed count for each item if the dialogue action is propose
#         # count should be parsed in the function

#         # TODO: added reasoning properly to the prompts.
#         count_split = count.split(" ")
#         for each in count_split:
#             item_count = each.split("=")
#             if (int(item_count[1]) > 0):
#                 extra_info += item_count[1] + " " + item_count[0] + ",and "
    
#         template_response = template_response.replace('xxx', extra_info)
#         # The way of parse count of item can be improved further by ordering the counts etc.

#     messages.append({"role": "user", "content": template_response})
#     return messages
