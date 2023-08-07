"""
Common independent utility functions for the llm_nego_plan_exps package.
"""

import sys
import importlib
import random

from agents import SingleLevelAgent, DualLevelAgent
from lang_models.gru import GRUModel
from data.word_corpus import WordCorpus

from registry import *


def get_datahandler(handler_id: str):
    if handler_id in DATA_HANDLER_REG.keys():
        module_class = DATA_HANDLER_REG[handler_id]
        DataHandler = getattr(importlib.import_module(
            module_class[0]), module_class[1])
        return DataHandler(handler_id)
    else:
        raise Exception(
            f'Data handler for {handler_id} not found, check registry.py')


def get_llm_api(api_id: str, key=None):
    if api_id is None:
        raise Exception(
            'An LLM Api must be provided through the "--llm_api" argument')
    elif api_id in LLM_API_REG.keys():
        module_class = LLM_API_REG[api_id]
        AnnotAPI = getattr(importlib.import_module(
            module_class[0]), module_class[1])
        return AnnotAPI(api_id)
    else:
        print(
            f'\nCannot find LLM in registry for argument --llm_api = {api_id}; Assuming {api_id} to be an OpenAI model ID\n')
        if key is None:
            raise Exception(
                'An API key must be provided to use the OpenAI generic API')

        module_class = LLM_API_REG['openai_generic']
        AnnotAPI = getattr(importlib.import_module(
            module_class[0]), module_class[1])
        return AnnotAPI(api_id, key)


def get_function_from_id(id: str, registry: dict):
    if id in registry.keys():
        module_class = registry[id]
        return getattr(importlib.import_module(module_class[0]), module_class[1])
    else:
        raise Exception(f'Function for id="{id}" not found, check registry.py')


def get_inst2annot_prompt_func(func_id: str):
    return get_function_from_id(func_id, INST2ANNOT_PROMPT_FUN_REG)


def get_annot_out_formatter_func(func_id: str):
    return get_function_from_id(func_id, INST_ANNOT2STR_PROMPT_FUN_REG)


def get_act2utt_prompt_func(func_id: str):
    return get_function_from_id(func_id, ACT2UTT_PROMPT_FUN_REG)


def get_utt2act_prompt_func(func_id: str):
    return get_function_from_id(func_id, UTT2ACT_PROMPT_FUN_REG)


def get_response_prompt_func(func_id: str):
    return get_function_from_id(func_id, RESPONSE_PROMPT_FUN_REG)


def load_rl_module(weights_path: str, corpus_data_pth: str):
    # if 'torch' not in sys.modules.keys():
    #     import torch
    import torch

    if torch.cuda.is_available():
        checkpoint = torch.load(weights_path)
    else:
        checkpoint = torch.load(weights_path, map_location=torch.device("cpu"))

    model_args = checkpoint["args"]

    # Verifies if CUDA is available and sets default device to be device_id.
    device_id=0
    if not model_args.cuda:
        device_id = None
    assert torch.cuda.is_available(), 'CUDA is not available'
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
    torch.cuda.set_device(device_id)

    corpus = WordCorpus(corpus_data_pth, freq_cutoff=model_args.unk_threshold, verbose=False)
    model = GRUModel(corpus.word_dict, corpus.item_dict, corpus.context_dict,
        corpus.output_length, model_args, device_id)

    model.load_state_dict(checkpoint['state_dict'])  # TODO: This will probably need to be updated
    return model

    # corpus_data_pth is forr training dataset, used to generater context/utterance embeddings
    return GRUModel(weights_path, corpus_data_pth)


def agent_builder(agent_type: str, agent_strategy: str, args, rl_module_weight_path=None, name: str='AI'):
    llm_api = get_llm_api(args.llm_api, args.llm_api_key)
    choice_prompt_func = get_response_prompt_func(args.llm_choice_prompt_func)

    if agent_type == 'llm_no_planning':
        response_prompt_func = get_response_prompt_func(args.llm_response_prompt_func)

        return SingleLevelAgent(model=llm_api, 
                                name=name,
                                rpf=response_prompt_func,
                                cpf=choice_prompt_func,
                                strategy = agent_strategy,
                                args=args)
    elif agent_type == 'llm_self_planning':
        parser_prompt_func = get_utt2act_prompt_func(args.utt2act_prompt_func)
        generator_prompt_func = get_act2utt_prompt_func(args.act2utt_prompt_func)

        response_prompt_func = get_response_prompt_func(args.llm_response_prompt_func)

        return DualLevelAgent(pg_model=llm_api,
                              p_prompt_func=parser_prompt_func,
                              g_prompt_func=generator_prompt_func,
                              planning_model=llm_api,
                              cpf=choice_prompt_func,
                              rpf=response_prompt_func,
                              strategy = agent_strategy,
                              name=name)
    elif agent_type == 'llm_rl_planning':
        parser_prompt_func = get_utt2act_prompt_func(args.utt2act_prompt_func)
        generator_prompt_func = get_act2utt_prompt_func(args.act2utt_prompt_func)

        assert rl_module_weight_path is not None, 'The --rl_module_weight_path argmuent must be specified when agent type is "llm_rl_planning"'
        assert args.corpus_source is not None, 'The --corpus_source argmuent must be specified when agent type is "llm_rl_planning"'
        rl_module = load_rl_module(rl_module_weight_path, args.corpus_source)
        
        return DualLevelAgent(pg_model=llm_api,
                              p_prompt_func=parser_prompt_func,
                              g_prompt_func=generator_prompt_func,
                              planning_model=rl_module,
                              cpf=choice_prompt_func,
                              name=name)
    else:
        raise ValueError(f'{agent_type} is not a recognized agent agent type!')


def set_seed(seed, torch_needed=False, np_needed=False):
    """Sets random seed everywhere."""
    if torch_needed:
        # if 'torch' not in sys.modules.keys():
        #     import torch
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)

    if np_needed:
        import numpy as np
        np.random.seed(seed)

    random.seed(seed)
