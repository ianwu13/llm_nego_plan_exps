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

from interactions import InteractionLogger, BotBotSelfPlay
from interactions.interaction_utils import Dialog
import utils


def main():
    parser = argparse.ArgumentParser(description='selfplaying script')
    # Interaction setup parameters
    parser.add_argument('--alice_model_file', type=str,
        help='Alice model file')
    parser.add_argument('--bob_model_file', type=str,
        help='Bob model file')
       
    parser.add_argument('--alice_type', type=str, default='llm_no_planning', 
        choices=['llm_no_planning', 'llm_self_planning', 'llm_rl_planning'],
        help='Agent type for Alice.')
    parser.add_argument('--bob_type', type=str, default='llm_no_planning', 
        choices=['llm_no_planning', 'llm_self_planning', 'llm_rl_planning'],
        help='Agent type for Bob.')
    parser.add_argument('--llm_api', type=str, default=None,
        help='Level at which the models interact [act|utt]')
    parser.add_argument('--llm_api_key', type=str, default=None,
        help='Key to be used when calling provided API')
    # Arguments which may be used depending on alice/bob_type
    parser.add_argument('--utt2act_prompt_func', type=str, default=None,
        help='Function ID from registry.py which converts utterance data into llm prompts for generating acts (Parser)')
    parser.add_argument('--act2utt_prompt_func', type=str, default=None,
        help='Function ID from registry.py which converts act data into llm prompts for generating utterances (Generator)')
    parser.add_argument('--rl_module_weight_path', type=str, default=None,
        help='Path to weights for the RL planning module')

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

    alice = utils.agent_builder(args.alice_type, args, name='Alice')
    bob = utils.agent_builder(args.bob_type, args, name='Bob')

    dialog = Dialog([alice, bob], args)
    logger = InteractionLogger(verbose=args.verbose, log_file=args.log_file)

    selfplay = BotBotSelfPlay(dialog, args.context_file, logger=logger, **args)
    selfplay.run()


if __name__ == '__main__':
    main()
