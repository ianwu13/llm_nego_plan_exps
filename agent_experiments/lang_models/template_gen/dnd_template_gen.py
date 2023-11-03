import random
dnd_template = {
    "greet": ["Hello", "Hey", "Hi"],
    "inquire": ["Do you have any good ideas about how to distribute these items?",
                "What do you think is the best way to allocate these items?",
                "What do you want to take?",
                "Do you have better ideas?"
                "What fo you need?",
                "What else can you do?",
                "Why don't you make me an offer"],
    "propose": ["I want to take xxx and you can take the rest.",
                "How about I take xxx and we evenly sitribute the rest?"],
    "insist": ["I still want it.",
               "I want more.",
               "I have to take at least one of them.",
               "That is my only offer"],
    "agree": ["Okay",
              "That is a great deal.",
              "Sounds great",
              "Great",
              "Deal",
              "I agree with it",
              "That works for me"],
    "disagree": ["Sorry it doesn't work for me.",
                 "No I can not accept that.",
                 "That isnot gonna work for me.",
                 "Sorry no.",
                 "Not gonna happen"],
    "unknown": ["Well, let me think about it for a while",
                "Hmm, give me some seconds to think about it."],
}

def parse_acts(da_str: str) -> list:
    # returns a list of dialogue acts
    # for example, 
    #       parse_acts("greet inquire firewood propose water=3")
    #             --> ["greet", "inquire firewood", "propose water=3"]
    
    # TODO LATER
    return []


# TODO NOW make one of these for each dialogue act label
# greet, inquire, propose, disagree, insist, agree, unknown

def tgen_greet():
    return "hello"

# TODO NOW (make one of these for each dialogue act label ^^^)

# Parse the dialogue act as the key and return a random response from the template dictionary
def get_temp(act, template_dict=dnd_template):
    temp_response = random.choice(template_dict[act])
    return temp_response

# generate one prompt for one dialogue act
def gen_rephrase_alone_prompts(da_str: str, count:str = "food=1 water=2 firewood=0",):

    system_sen =  f'Return the rephrased statement used in negotiation scenario.' 
    messages = [{"role": "system", "content": system_sen }]

    # get a random template response for a dialogue action
    template_response = get_temp(da_str)

    extra_info = ""
    if da_str == "propose":
        extra_info = ""
        # add extra_info with the parsed count for each item if the dialogue action is propose
        # count should be parsed in the function
        count_split = count.split(" ")
        for each in count_split:
            item_count = each.split("=")
            if (int(item_count[1]) > 0):
                extra_info += item_count[1] + " " + item_count[0] + ", "
    
        template_response = template_response.replace('xxx', extra_info)
        # The way of parse count of item can be improved further by ordering the counts etc.

    messages.append({"role": "user", "content": template_response})
    return messages

# prompts to rephrase all dialogue acts together at once
def gen_rephrase_prompts(da_str: str)-> list[str]:
    acts_list = parse_acts(da_str)
    # TODO LATER
    prompts = []
    for each in acts_list:
        prompts.append(gen_rephrase_alone_prompts(each))
    return prompts

