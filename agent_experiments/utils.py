"""
Common independent utility functions for the llm_nego_plan_exps package.
"""

import importlib
import json
import os
from registry import *


def get_datahandler(handler_id: str):
    if handler_id in DATA_HANDLER_REG.keys():
        return importlib.import_module(DATA_HANDLER_REG[handler_id])
    else:
        raise Exception(f'Data handler for {handler_id} not found, check registry.py')


def get_llm_api(api_id: str):
    if api_id in LLM_API_REG.keys():
        AnnotAPI = importlib.import_module(LLM_API_REG[api_id])
        return AnnotAPI()
    else:
        print(f'\nCannot find LLM in registry for argument --llm_api = {api_id}; Assuming {api_id} to be an OpenAI model ID\n')
        AnnotAPI = importlib.import_module(LLM_API_REG['openai_generic'])
        return AnnotAPI(api_id, MY_OPENAI_KEY)


def get_inst2annot_prompt_func(func_id: str):
    if func_id in I2ANNOT_PROMPT_FUN_REG.keys():
        return importlib.import_module(I2ANNOT_PROMPT_FUN_REG[func_id])
    else:
        raise Exception(f'Function for {func_id} not found, check registry.py')


def get_act2utt_prompt_func(func_id: str):
    if func_id in ACT2UTT_PROMPT_FUN_REG.keys():
        return importlib.import_module(ACT2UTT_PROMPT_FUN_REG[func_id])
    else:
        raise Exception(f'Function for {func_id} not found, check registry.py')


def get_utt2act_prompt_func(func_id: str):
    if func_id in UTT2ACT_PROMPT_FUN_REG.keys():
        return importlib.import_module(UTT2ACT_PROMPT_FUN_REG[func_id])
    else:
        raise Exception(f'Function for {func_id} not found, check registry.py')


# TODO: FROM E2E, SHOULD UPDATE
def set_seed(seed):
    """Sets random seed everywhere."""
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)


# TODO: FROM E2E, SHOULD UPDATE
def load_model(file_name):
    """Reads model from a file."""

    if torch.cuda.is_available():
        checkpoint = torch.load(file_name)
    else:
        checkpoint = torch.load(file_name, map_location=torch.device("cpu"))

    model_args = checkpoint["args"]

    device_id = use_cuda(model_args.cuda)
    corpus = data.WordCorpus(model_args.data, freq_cutoff=model_args.unk_threshold, verbose=False)
    model = DialogModel(corpus.word_dict, corpus.item_dict, corpus.context_dict,
        corpus.output_length, model_args, device_id)

    model.load_state_dict(checkpoint['state_dict'])
    return model
