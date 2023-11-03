import random
casino_template_dnd_format = {
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

# smalltalk, empathy coordination, no need, elicit preference, undervalue, vouch fairness, express preference, propose, disagree, agree, unknown
casino_template_cust_format = {
    "smalltalk": ["Hello", "Hey", "Hi", "How are you?"],
    "empathy coordination": ["Do you have any good ideas about how to distribute these items?",
                "What do you think is the best way to allocate these items?",
                "What do you want to take?",
                "Do you have better ideas?"
                "What fo you need?",
                "What else can you do?",
                "Why don't you make me an offer"],
    "no need": ["Sorry I dont need that",
                 "we already have plenty of that"],
    "elicit preference": ["I still want it.",
               "I want more.",
               "I have to take at least one of them.",
               "That is my only offer"],
    "undervalue": ["Do you have help carrying all that extra xxx? Could be heavy",
                   "Are you sure you need xxx?",
                   "I don't think that you need xxx as much as you describe.",
                   "It will be fine if you don't have a lot of xxx"],
    "vouch fairness": ["Does the proposal sounds fair to you?",
               "I want to make sure it works for both of us",
               "I wondered whether the proposal benefit us at the same time, I want to take xxx and you can take the rest."],
    "express preference": ["I prefer xxx than yyyy",
                           "I really want more xxx",
                           "xxx is really important for me"],
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
def tgen_greet():
    return "hello"


# TODO NOW (make one of these for each dialogue act label ^^^)


# def gen_rephrase_alone_prompts(da_str: str):
#     # prompts to rephrase each dialogue act alone
#     acts_list = parse_acts(da_str)
#     # TODO LATER


# def gen_rephrase_prompts(da_str: str):
#     # prompts to rephrase all dialogue acts together at once
#     acts_list = parse_acts(da_str)
#     # TODO LATER

# Parse the dialogue act as the key and return a random response from the template dictionary
def get_temp(act, template_dict=casino_template_cust_format):
    temp_response = random.choice(template_dict[act])
    return temp_response

# generate one prompt for one dialogue act
# for casino we might need reasoning?
def gen_rephrase_alone_prompts(da_str: str, count:str = "food=1 water=2 firewood=0", reasons:str = " "):

    system_sen =  f'Return the rephrased statement used in negotiation scenario.' 
    messages = [{"role": "system", "content": system_sen }]

    # get a random template response for a dialogue action
    template_response = get_temp(da_str)

    extra_info = ""
    # TODO: add more info based on different dialogue act
    if da_str == "express preference":
        extra_info = ""
        # add extra_info with the parsed count for each item if the dialogue action is propose
        # count should be parsed in the function

        # TODO: added reasoning properly to the prompts.
        count_split = count.split(" ")
        for each in count_split:
            item_count = each.split("=")
            if (int(item_count[1]) > 0):
                extra_info += item_count[1] + " " + item_count[0] + ",and "
    
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

