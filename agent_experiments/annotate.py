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

from registry import LLM_API_REG, I2ANNOT_PROMPT_FUN_REG, DATA_HANDLER_REG

from storage.utilities.open_ai import MY_OPENAI_KEY


def main():
    # TODO - START
    parser = argparse.ArgumentParser(description='script to annotate data')
    
    # ARGS IDEAS:
        # Dataset to annotate
        # Destination for annotated data
        # Annotation method (llm or regex parser)
            # if LLM need prompt format template, also which llm to use?

    parser.add_argument('--dataset', type=str, choices = ['dnd','casino'],
        help='dataset')
    
    parser.add_argument('--input_file', type=str, default='data/conversion/data.txt',
        help='input file')
    
    parser.add_argument('--output_file', type=str, default='dummy_output.txt',
        help='destination for output file')
    
    parser.add_argument('--inst_to_prompt_funct', type=str, default='cum', choices = ['sep','cum'],
        help='function to convert instance to prompt, based on the dataset')
    
    parser.add_argument('--annot_method', type=str, default='llm',
        help='Annotation method (llm or regex parser)')    

    parser.add_argument('--llm_type', type=str, default='openai_generic',
        help='llm types')
    
    parser.add_argument('--open_ai_model_type', type=str, default='chat_bot', choices = ['chat_bot', 'text_generate'],
        help='model name from open_ai to generate annotation')

    args = parser.parse_args()

    print("parsing all done")

    # Get dataset here

    if args.dataset in DATA_HANDLER_REG.keys():
        print("get in")
        DataHandler = importlib.import_module('data.dealornodeal').DNDHandler
        # DataHandler = importlib.import_module(DATA_HANDLER_REG[args.dataset])
    else:
        raise Exception("Dataset name not recgonized")
    
    dataset = DataHandler('place_hoder_name','place_hoder_args')
    
    # i2p_funct = importlib.import_module(I2ANNOT_PROMPT_FUN_REG[args.inst_to_prompt_funct])

    if args.annot_method == 'llm':
        print("check llm")
        if args.llm_type in LLM_API_REG.keys():
            # AnnotAPI = importlib.import_module(LLM_API_REG[args.llm_type])
            # annot_api = AnnotAPI()
            pass
        else:
            # AnnotAPI = importlib.import_module(LLM_API_REG['openai_generic'])
            # annot_api = AnnotAPI(args.llm_type, MY_OPENAI_KEY)
            pass
    else:
        raise NotImplementedError("only llm annotation is currently implemented")
    
    # i2p_funct = importlib.import_module(I2ANNOT_PROMPT_FUN_REG[args.inst_to_prompt_funct])

    annot_api = importlib.import_module("llm_apis.open_ai").OpenAI_Api
    openai_api = annot_api(MY_OPENAI_KEY)
    annotator = Annotator(dataset, openai_api, args.input_file, args.output_file, args.inst_to_prompt_funct, args.open_ai_model_type)
    # annotator = Annotator(dataset, i2p_funct, annot_api, args.output_file)

    annotator.annotate()

    print("annotation all done")


if __name__ == '__main__':
    main()
