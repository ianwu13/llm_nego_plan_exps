# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""
An util to negotiate with AI.
"""

import argparse

from interactions import BotHumanChat
from interactions.interaction_utils import Dialog, InteractionLogger
import utils


def main():
    parser = argparse.ArgumentParser(description='chat utility')
    # Interaction setup parameters
    parser.add_argument('--model_file', type=str,
        help='model file')
    parser.add_argument('--ai_starts', action='store_true', default=False,
        help='allow AI to start the dialog')
        
    parser.add_argument('--ai_type', type=str, default='llm_no_planning', 
        choices=['llm_no_planning', 'llm_self_planning', 'llm_rl_planning'],
        help='Agent type for the AI agent.')
    parser.add_argument('--llm_api', type=str, default=None,
        help='Level at which the models interact [act|utt]')
    parser.add_argument('--llm_api_key', type=str, default=None,
        help='Key to be used when calling provided API')
    # Arguments which may be used depending on ai_type
    parser.add_argument('--utt2act_prompt_func', type=str, default=None,
        help='Function ID from registry.py which converts utterance data into llm prompts for generating acts (Parser)')
    parser.add_argument('--act2utt_prompt_func', type=str, default=None,
        help='Function ID from registry.py which converts act data into llm prompts for generating utterances (Generator)')
    parser.add_argument('--llm_response_prompt_func', type=str, default=None,
        help='Function ID from registry.py which generates a prompt for the llm api (if used) to generate the next response in the dialogue')
    parser.add_argument('--rl_module_weight_path', type=str, default=None,
        help='Path to weights for the RL planning module')

    parser.add_argument('--context_file', type=str, default='',
        help='context file (scenarios for each dialog)')
    parser.add_argument('--ref_text', type=str,
        help='file with the reference text')
    # Logs
    parser.add_argument('--log_file', type=str, default='',
        help='log dialogs to file for training')
    # Misc args
    parser.add_argument('--seed', type=int, default=1,
        help='random seed')
    # args to be used if context file is not provided (context for each dialogue will be entered manually by user)
    parser.add_argument('--num_types', type=int, default=3,
        help='number of object types')
    parser.add_argument('--num_objects', type=int, default=6,
        help='total number of objects')
    parser.add_argument('--max_score', type=int, default=10,
        help='max score per object')

    args = parser.parse_args()

    utils.set_seed(args.seed, torch_needed=True, np_needed=True)

    human = HumanAgent()
    ai = utils.agent_builder(args.ai_type, args, name='AI')

    agents = [ai, human] if args.ai_starts else [human, ai]

    dialog = Dialog(agents, args)
    logger = InteractionLogger(verbose=True, log_file=args.log_file)

    chat = BotHumanChat(dialog, args.context_file, logger=logger)
    chat.run()


if __name__ == '__main__':
    main()
