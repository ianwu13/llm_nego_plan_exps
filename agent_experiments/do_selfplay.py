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

from interactions import BotBotSelfPlay
from interactions.interaction_utils import Dialog, InteractionLogger
import utils


def main():
    parser = argparse.ArgumentParser(description='selfplaying script')
    # Interaction setup parameters
    parser.add_argument('--dataset', type=str, default='dnd', 
        choices=['dnd', 'casino'],
        help='Which Dataset is using')  
    parser.add_argument('--alice_type', type=str, default='llm_no_planning', 
        choices=['llm_no_planning', 'llm_self_planning', 'llm_rl_planning'],
        help='Agent type for Alice.')
    parser.add_argument('--alice_strategy', type=str, default='generic',
        choices=['generic', 'selfish', 'fair'],
        help='agent_strategy/personality')
    parser.add_argument('--bob_type', type=str, default='llm_no_planning', 
        choices=['llm_no_planning', 'llm_self_planning', 'llm_rl_planning'],
        help='Agent type for Bob.')
    parser.add_argument('--bob_strategy', type=str, default='generic',
        choices=['generic', 'selfish', 'fair'],
        help='agent_strategy/personality')
       
    parser.add_argument('--llm_api', type=str, default=None,
        help='Level at which the models interact [act|utt]')
    parser.add_argument('--llm_api_key', type=str, default=None,
        help='Key to be used when calling provided API')
    parser.add_argument('--utt2act_prompt_func', type=str, default=None,
        help='Function ID from registry.py which converts utterance data into llm prompts for generating acts (Parser)')
    parser.add_argument('--act2utt_prompt_func', type=str, default=None,
        help='Function ID from registry.py which converts act data into llm prompts for generating utterances (Generator)')
    parser.add_argument('--llm_response_prompt_func', type=str, default=None,
        help='Function ID from registry.py which generates a prompt for the llm api (if used) to generate the next response in the dialogue')
    parser.add_argument('--llm_choice_prompt_func', type=str, default=None,
        help='Function ID from registry.py which generates a prompt for the llm api (if used) to generate the final choice for a dialogue')
    
    parser.add_argument('--alice_model_file', type=str, default=None,
        help='Alice model file')
    parser.add_argument('--bob_model_file', type=str, default=None,
        help='Bob model file')
    parser.add_argument('--corpus_source', type=str, default=None,
        help='Path to file used to generate the corpus for GRU model (MUST BE THE SAME AS FILE USED FOR TRAINING GRU MODULE)')

    parser.add_argument('--max_turns', type=int, default=20,
        help='maximum number of turns in a dialog')
    parser.add_argument('--context_file', type=str,
        help='context file (scenarios for each dialog)')
    parser.add_argument('--ref_text', type=str,
        help='file with the reference text')
    # Logs
    parser.add_argument('--log_file', type=str, default='',
        help='log dialogs to file for training')
    # Misc args
    parser.add_argument('--verbose', action='store_true', default=False,
        help='print out converations')
    parser.add_argument('--seed', type=int, default=1,
        help='random seed')

    args = parser.parse_args()

    utils.set_seed(args.seed, torch_needed=True, np_needed=True)

    alice = utils.agent_builder(args.alice_type, args.alice_strategy, args, rl_module_weight_path=args.alice_model_file, name='Alice')
    
    
    
    bob = utils.agent_builder(args.bob_type, args.bob_strategy, args, rl_module_weight_path=args.bob_model_file, name='Bob')

    dialog = Dialog([alice, bob], args)
    logger = InteractionLogger(args.dataset, verbose=args.verbose, log_file=args.log_file)

    # selfplay = BotBotSelfPlay(dialog, args.dataset, args.context_file, logger=logger, **vars(args))
    selfplay = BotBotSelfPlay(dialog, args.dataset, args.context_file, logger=logger)
    selfplay.run()


if __name__ == '__main__':
    main()
