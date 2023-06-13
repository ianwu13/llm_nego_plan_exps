# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""
Selfplaying util.
"""

import argparse
import pdb
import re
import random
import importlib

import numpy as np
import torch
from torch import optim
from torch import autograd
import torch.nn as nn

from data import Annotator

from registry import LLM_API_REG, I2P_REG, DATA_HANDLER_REG

from storage.utilities.open_ai import MY_OPENAI_KEY


def main():
    # TODO - START
    parser = argparse.ArgumentParser(description='script to annotate data')
    # parser.add_argument('--alice_model_file', type=str,
    #     help='Alice model file')
    # parser.add_argument('--bob_model_file', type=str,
    #     help='Bob model file')
    # parser.add_argument('--context_file', type=str,
    #     help='context file')
    # parser.add_argument('--temperature', type=float, default=1.0,
    #     help='temperature')
    # parser.add_argument('--verbose', action='store_true', default=False,
    #     help='print out converations')
    # parser.add_argument('--seed', type=int, default=1,
    #     help='random seed')
    # parser.add_argument('--score_threshold', type=int, default=6,
    #     help='successful dialog should have more than score_threshold in score')
    # parser.add_argument('--max_turns', type=int, default=20,
    #     help='maximum number of turns in a dialog')
    # parser.add_argument('--log_file', type=str, default='',
    #     help='log dialogs to file for training')
    # parser.add_argument('--smart_alice', action='store_true', default=False,
    #     help='make Alice smart again')
    # parser.add_argument('--fast_rollout', action='store_true', default=False,
    #     help='to use faster rollouts')
    # parser.add_argument('--rollout_bsz', type=int, default=100,
    #     help='rollout batch size')
    # parser.add_argument('--rollout_count_threshold', type=int, default=3,
    #     help='rollout count threshold')
    # parser.add_argument('--smart_bob', action='store_true', default=False,
    #     help='make Bob smart again')
    # parser.add_argument('--ref_text', type=str,
    #     help='file with the reference text')
    # parser.add_argument('--domain', type=str, default='object_division',
    #     help='domain for the dialogue')
    
    # ARGS IDEAS:
        # Dataset to annotate
        # Destination for annotated data
        # Annotation method (llm or regex parser)
            # if LLM need prompt format template, also which llm to use?

    parser.add_argument('--dataset', type=str, choice = ['DND','CaSiNo'],
        help='dataset')
    
    parser.add_argument('--output_file', type=str,
        help='destination for output file')
    
    parser.add_argument('--inst_to_prompt_funct', type=str, default='func_1',
        help='function to convert instance to prompt, based on the dataset')
    
    parser.add_argument('--annot_method', type=str, default='llm',
        help='Annotation method (llm or regex parser)')    

    parser.add_argument('--llm_type', type=str, default='falcon',
        help='llm types')

    args = parser.parse_args()

    print("parsing all done")

    # Get dataset here

    if args.dataset in DATA_HANDLER_REG.keys():
        DataHandler = importlib.import_module(DATA_HANDLER_REG[args.dataset])
    else:
        raise Exception("Dataset name not recgonized")
    dataset = DataHandler()

    i2p_funct = importlib.import_module(I2P_REG[args.inst_to_prompt_funct])

    if args.annot_method == 'llm':
        if args.llm_type in LLM_API_REG.keys():
            AnnotAPI = importlib.import_module(LLM_API_REG[args.llm_type])
            annot_api = AnnotAPI()
        else:
            AnnotAPI = importlib.import_module(LLM_API_REG['openai_generic'])
            annot_api = AnnotAPI(args.llm_type, MY_OPENAI_KEY)
    else:
        raise NotImplementedError("only llm annotation is currently implemented")

    annotator = Annotator(dataset, i2p_funct, annot_api, args.output_file)

    annotator.annotate()

    print("annotation all done")


if __name__ == '__main__':
    main()
