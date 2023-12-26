import random

from lang_models.template_gen.template_utils import parse_acts


DND_ITEMS = ['books', 'hats', 'balls']
DND_LABELS = [
    'greet',
    'inquire',
    'propose',
    'insist',
    'disagree',
    'agree',
    'unknown',
]

def tgen_greet(slots_list: list):
    return random.choice(
        ["Hello!", 
        "Hey!", 
        "Hi!", 
        "How are you?", 
        "Hi, how are you?"])

def tgen_inquire(slots_list: list):
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

def tgen_insist(slots_list: list):
    if not slots_list:  # slots_list is empty (This should not happen)
        return ""
        
    s_vals, s_no_vals = seperate_slots_w_values(slots_list)
    if s_vals:  # Will ignore s_no_vals in this case
        if len(s_vals) == 1:
            proposal_counts_str = f'{s_vals[0][1]} {s_vals[0][0]}'
        else:
            proposal_counts_str = ', and'.join([', '.join(s_vals[:-1]), s_vals[-1]])
    elif s_no_vals:
        if len(s_no_vals) == 1:
            proposal_counts_str = s_no_vals[0]
        else:
            proposal_counts_str = ', and'.join([', '.join(s_no_vals[:-1]), s_no_vals[-1]])

    return random.choice([
        f"No, I really need {proposal_counts_str}.",
        f"I insist that I get {proposal_counts_str}."])

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
        "That works for me"])

def tgen_unknown(slots_list: list):
    return random.choice([
        "Let's negotiate some more.",
        "Hmm, I'm not sure."])

dnd_template_index = {
    'greet': tgen_greet,
    'inquire': tgen_inquire,
    'propose': tgen_propose,
    'insist': tgen_insist,
    'disagree': tgen_disagree,
    'agree': tgen_agree,
    'unknown': tgen_unknown,
}

# prompts to rephrase all dialogue acts together at once
def gen_rephrase_prompt(da_toks: list, dialogue: list)-> list:
    acts_list = parse_acts(da_toks, DND_LABELS, DND_ITEMS)
    template_gens = [dnd_template_index[act[0]](act[1]) for act in acts_list]
    full_template_gen = ' '.join(template_gens)

    usr_prompt = f'Dialogue history:\n"{" ".join(dialogue)}"\n\nRephrase and improve this sentence to respond to fit the dialogue history:\n"{full_template_gen}"'

    messages = [
        {"role": "system", "content": "You are a helping the user in rephrasing simple sentences to be more expressive in the contet of negotiation. Rephrase the sentences to be fluid, expressive, and concise."},
        {"role": "user", "content": usr_prompt}
    ]
    return messages

