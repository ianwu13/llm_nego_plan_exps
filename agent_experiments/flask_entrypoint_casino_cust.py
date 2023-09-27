import random

from flask import Flask
from flask import request
from flask import json
import torch
import utils

app = Flask(__name__)

# globals: to be initialized in initial_setup - a common storage variable for everything, including initiated models and current states of each of the users.
STORAGE = {
    "static": {},
    "users": {}
}
SERVER_STATUS = "Not Ready"

DIALOGUE_COUNT_CAP = 8

# DATASET SPECIFIC #############################################
CTX_PAIRS_FILE = "flask_utils/mod_cxt_pairs_casino_cust.json"

llm_api_key = ''  # TODO FILL LOCALLY
LLM_API = utils.get_llm_api('gpt-3.5-turbo-0613', llm_api_key)

LLM_NO_PLANNING_RESPONSE_FUNCT = utils.get_response_prompt_func('dia_resp_slagent_chatcomp_casino') 

PARSER_FUNC = utils.get_utt2act_prompt_func('final_utt2act_casino_cust')
GENERATOR_FUNCT = utils.get_act2utt_prompt_func('casino_a2u_prompt')

LLM_W_PLANNING_RESPONSE_FUNCT = utils.get_response_prompt_func('act_act_chatcomp_casino_cust_form')

MODEL_CHOICE_FUNCT = utils.get_response_prompt_func('choice_slagent_chatcomp_casino')

GRU_TRAINING_FILE = "data/final_datasets/casino_cust_valid/train_fixed.txt"

GRU_FILES = [
    "casino_custformat_supervised_30ep.pt",
    "casino_custform_rl_selfish_4ep_rw_own_points.pt",
    "casino_custform_rl_fair_4ep_rw_combine50_50.pt",
]
GRU_MODELS = []
# DATASET SPECIFIC ##################################################

# MODEL_NAMES
# ['np_generic', 'np_selfish', 'np_fair', 'sp_generic', 'sp_selfish', 'sp_fair', 'rl_supervised', 'rl_selfish', 'rl_fair']

MODEL_CONFIGS = {
    'np_generic': {
        'agent_type': 'llm_no_planning',
        'strategy': 'generic',
        'model': LLM_API,
        'rpf': LLM_NO_PLANNING_RESPONSE_FUNCT,
        'cpf': MODEL_CHOICE_FUNCT,
    },
    'np_selfish': {
        'agent_type': 'llm_no_planning',
        'strategy': 'selfish',
        'model': LLM_API,
        'rpf': LLM_NO_PLANNING_RESPONSE_FUNCT,
        'cpf': MODEL_CHOICE_FUNCT,
    },
    'np_fair': {
        'agent_type': 'llm_no_planning',
        'strategy': 'fair',
        'model': LLM_API,
        'rpf': LLM_NO_PLANNING_RESPONSE_FUNCT,
        'cpf': MODEL_CHOICE_FUNCT,
    },
    'sp_generic': {
        'agent_type': 'llm_self_planning',
        'strategy': 'generic',
        'pg_model': LLM_API,
        'planning_model': LLM_API,
        'p_prompt_func': PARSER_FUNC,
        'g_prompt_func': GENERATOR_FUNCT,
        'rpf': LLM_W_PLANNING_RESPONSE_FUNCT,
        'cpf': MODEL_CHOICE_FUNCT,
    },
    'sp_selfish': {
        'agent_type': 'llm_self_planning',
        'strategy': 'selfish',
        'pg_model': LLM_API,
        'planning_model': LLM_API,
        'p_prompt_func': PARSER_FUNC,
        'g_prompt_func': GENERATOR_FUNCT,
        'rpf': LLM_W_PLANNING_RESPONSE_FUNCT,
        'cpf': MODEL_CHOICE_FUNCT,
    },
    'sp_fair': {
        'agent_type': 'llm_self_planning',
        'strategy': 'fair',
        'pg_model': LLM_API,
        'planning_model': LLM_API,
        'p_prompt_func': PARSER_FUNC,
        'g_prompt_func': GENERATOR_FUNCT,
        'rpf': LLM_W_PLANNING_RESPONSE_FUNCT,
        'cpf': MODEL_CHOICE_FUNCT,
    },
    'rl_supervised': {
        'agent_type': 'llm_rl_planning',
        'pg_model': LLM_API,
        'planning_model': 0,
        'p_prompt_func': PARSER_FUNC,
        'g_prompt_func': GENERATOR_FUNCT,
        'cpf': MODEL_CHOICE_FUNCT,
    },
    'rl_selfish': {
        'agent_type': 'llm_rl_planning',
        'pg_model': LLM_API,
        'planning_model': 1,
        'p_prompt_func': PARSER_FUNC,
        'g_prompt_func': GENERATOR_FUNCT,
        'cpf': MODEL_CHOICE_FUNCT,
    },
    'rl_fair': {
        'agent_type': 'llm_rl_planning',
        'pg_model': LLM_API,
        'planning_model': 2,
        'p_prompt_func': PARSER_FUNC,
        'g_prompt_func': GENERATOR_FUNCT,
        'cpf': MODEL_CHOICE_FUNCT,
    },
}


def load_rl_models():
    """
    Load models.
    """
    global GRU_FILES
    global GRU_MODELS

    for mod_name in GRU_FILES:
        mod_path = os.path.join("models", mod_name)
        mod = utils.load_rl_module(mod_path)
        GRU_MODELS.append(mod)


def get_model(name):
    """
    Load models.
    """
    global MODEL_CONFIGS

    config = MODEL_CONFIGS[name]

    agent_type = config['agent_type']
    llm_api = config['model']
    choice_prompt_func = config['cpf']

    if agent_type == 'llm_no_planning':
        agent_strategy = config['strategy']
        response_prompt_func = config['rpf']

        return SingleLevelAgent(model=llm_api,
                                rpf=response_prompt_func,
                                cpf=choice_prompt_func,
                                strategy=agent_strategy,
                                name=name,
                                args=None)
    elif agent_type == 'llm_self_planning':
        agent_strategy = config['strategy']
        response_prompt_func = config['rpf']

        parser_prompt_func = config['p_prompt_func']
        generator_prompt_func = config['g_prompt_func']

        return DualLevelAgent(pg_model=llm_api,
                              p_prompt_func=parser_prompt_func,
                              g_prompt_func=generator_prompt_func,
                              planning_model=llm_api,
                              cpf=choice_prompt_func,
                              rpf=response_prompt_func,
                              strategy=agent_strategy,
                              name=name)
    elif agent_type == 'llm_rl_planning':
        global GRU_MODELS
        planning_model = GRU_MODELS[config['planning_model']]

        parser_prompt_func = config['p_prompt_func']
        generator_prompt_func = config['g_prompt_func']

        return DualLevelAgent(pg_model=llm_api,
                              p_prompt_func=parser_prompt_func,
                              g_prompt_func=generator_prompt_func,
                              planning_model=rl_module,
                              cpf=choice_prompt_func,
                              name=name)
    else:
        raise ValueError(f'{agent_type} is not a recognized agent type!')


def initial_setup():
    """
    Initial setup for the server
      - Load all the models.
      - Load context pairs and be ready for answering the requests.
    """
    global STORAGE
    global SERVER_STATUS

    global CTX_PAIRS_FILE
    global MODEL_CONFIGS

    # load potential model, context pairs from the json.
    with open(CTX_PAIRS_FILE, "r") as f:
        STORAGE["static"]["mod_cxt_all"] = [tuple(item) for item in json.load(f)[
            "mod_cxt_pairs"]]  # TODO

    # load all the models - mod is the model object that will be used for reading, writing, etc.
    load_rl_models()
    name2mod = list(MODEL_CONFIGS.keys())  # load_models()
    STORAGE["static"]["name2mod"] = name2mod

    # initialize the storage for users
    # set of (model, context) pairs that have been used.
    STORAGE["users"]["mod_cxt_used"] = set()
    # dict from random IDs to everything related to a specific user, model, cxt, and all lioness interaction.
    STORAGE["users"]["user_data"] = {}

    # mark the server as ready

    SERVER_STATUS = "Ready"


@app.route('/setup_new_user/', methods=['POST'])
def setup_new_user():
    """
    Setup for a new user - build the connection.
     - return a new random id, and human context, for the user.
     - save the model, context and random id in the storage.
     - mark this triplet as used.
    """
    global STORAGE
    global DIALOGUE_COUNT_CAP

    if SERVER_STATUS != "Ready":
        # server is not yet ready with the initial setup.
        data = {}
        data["status"] = "Error"
        data["error_description"] = "Server is not ready yet. Please wait for a few seconds and try again."
        return json.dumps(data)

    if len(STORAGE["users"]["user_data"]) >= DIALOGUE_COUNT_CAP:
        # server is not yet ready with the initial setup.
        data = {}
        data["status"] = "Error"
        data["error_description"] = "Concurrent dialogue count exceeded. Please wait for another conversation to end and try again."
        return json.dumps(data)

    # pick 10 random digits from 1 to 9 (both included) and join them as the randomId for the user
    randomId = ''.join([str(random.randint(1, 9)) for _ in range(10)])

    # pick a new model, cxt pair that is not in mod_cxt_used
    chosen_mod_cxt = None
    for mod_cxt_pair in STORAGE["static"]["mod_cxt_all"]:
        if mod_cxt_pair not in STORAGE["users"]["mod_cxt_used"]:
            chosen_mod_cxt = mod_cxt_pair
            break

    # if no new model, cxt pair is available, pick a pair at random
    if not chosen_mod_cxt:
        # choose any model and a cxt pair at random
        chosen_mod_cxt = random.choice(STORAGE["static"]["mod_cxt_all"])

    # update the storage appropriately
    STORAGE["users"]["mod_cxt_used"].add(chosen_mod_cxt)
    usr_model = get_model(chosen_mod_cxt[0])
    usr_model.feed_context(chosen_mod_cxt[1])

    STORAGE["users"]["user_data"][randomId] = {
        "model": usr_model,
        "cxt": chosen_mod_cxt[1],
        "lioness": {},  # start an account for this user in the storage
    }

    # output
    data = {}
    data["status"] = "Success"
    data["randomId"] = randomId
    data["hct"] = " ".join(chosen_mod_cxt[1].split()[:6])
    # utils.encode(" ".join(chosen_mod_cxt[1].split()[6:]), key="")  # TODO - IDK WHAT THIS IS
    data["agct"] = ''
    # utils.encode(chosen_mod_cxt[0], key="")  # TODO - IDK WHAT THIS IS
    data["agm"] = ''
    return json.dumps(data)


@app.route('/model_resp/', methods=['POST'])
def model_resp():
    """
    Get model response - interface for all the cases possible. The method in utils processes the request, and returns the response object (that is sent out), and storage obj (that is used to update the lioness storage for the user).

    Input payload must contain randomId, model, cxt, and any human utterance.
    """

    global STORAGE
    if SERVER_STATUS != "Ready":
        # server is not yet ready with the initial setup.
        data = {}
        data["status"] = "Error"
        data["error_description"] = "Server is not ready yet. Please wait for a few seconds and try again."
        return json.dumps(data)

    payload = json.loads(request.get_data().decode('utf-8'))

    # check if the randomId is valid
    if payload["randomId"] not in STORAGE["users"]["user_data"]:
        # invalid randomId
        data = {}
        data["status"] = "Error"
        data["error_description"] = "Invalid randomId. Please check the randomId and try again."
        return json.dumps(data)

    # get the model and cxt from the storage
    model_obj = STORAGE["users"]["user_data"][payload["randomId"]]["model"]
    cxt = STORAGE["users"]["user_data"][payload["randomId"]]["cxt"]

    # Read in human input for model
    if payload["human_utt"]:
        model_obj.read(payload["human_utt"].split())

    # see if the human has already outputted a selection token
    if '<selection>' in payload["human_utt"]:
        # agent response is just the selection token
        resp = ["<selection>"]
    else:
        resp = model_obj.write()

    # add the agent response to the conversation
    utt_obj = {
        "name": "agent",
        "sent": " ".join(resp),
    }

    # prepare outputs
    out_resp_obj = {
        "resp": utils.make_safe(" ".join(resp)),
    }

    # Model has indicated a selection
    if '<selection>' in utt_obj["sent"]:
        agent_choice = model_obj.choose()
        agent_choice = [utils.make_safe(c) for c in agent_choice]
        out_resp_obj["agent_choice"] = agent_choice

    # output
    data = {}
    data["status"] = "Success"
    data["randomId"] = payload["randomId"]
    data["response"] = out_resp_obj
    return json.dumps(data)


@app.route('/reset/', methods=['POST'])
def reset():
    """
    Reset the internal states, as if no user has been connected to the server yet, after the server has been started. You can still keep the models loaded.
    This is useful for debugging.
    """
    global STORAGE

    if SERVER_STATUS != "Ready":
        # server is not yet ready with the initial setup.
        data = {}
        data["status"] = "Error"
        data["error_description"] = "Server is not ready yet. Please wait for a few seconds and try again."
        return json.dumps(data)

    # re-initialize the storage for users

    STORAGE["users"]["mod_cxt_used"] = set()
    STORAGE["users"]["user_data"] = {}

    # output
    data = {}
    data["status"] = "Success"
    return json.dumps(data)


@app.route('/report_stats/', methods=['POST'])
def report_stats():
    """
    Report basic stats about the current state of the server.
      - # of models, contexts, etc.
      - how many users have connected so far.
      - how many users are remaining, so on.
    This is useful for debugging.
    """

    if SERVER_STATUS != "Ready":
        # initial setup has not been done yet.
        data = {}
        data["status"] = "Error"
        data["error_description"] = "Server is not ready yet. Please wait for a few seconds and try again."
        return json.dumps(data)

    # compute all useful stats from STORAGE
    data = {}
    data["status"] = "Success"
    data["server_status"] = SERVER_STATUS
    data["num_models"] = len(STORAGE["static"]["name2mod"])
    data["model_names"] = STORAGE["static"]["name2mod"]
    data["num_mod_cxt_used"] = f'{len(STORAGE["users"]["mod_cxt_used"])} / {len(STORAGE["static"]["mod_cxt_all"])}'
    data["num_users_served"] = len(STORAGE["users"]["user_data"])

    # print a sample user data
    if len(STORAGE["users"]["user_data"]) > 0:
        print("Sample user data:")
        print(list(STORAGE["users"]["user_data"].values())[0])

    return json.dumps(data)


# run initial setup
initial_setup()


def create_app():
    return app
