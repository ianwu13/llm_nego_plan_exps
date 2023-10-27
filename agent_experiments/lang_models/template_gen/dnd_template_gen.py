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


def gen_rephrase_prompts(da_str: str):
    # prompts to rephrase all dialogue acts together at once
    acts_list = parse_acts(da_str)
    # TODO LATER
