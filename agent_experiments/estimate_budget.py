"""
Annotate data using LLM apis
"""

import argparse
import pdb

from data import Annotator
import utils


def main():
    parser = argparse.ArgumentParser(description='script to annotate data')
    parser.add_argument('--dataset', type=str, choices=['dnd','casino'],
        help='Dataset handler ID')
    parser.add_argument('--inst_to_prompt_funct', type=str, default='example',
        help='function to convert instance (set of utterances) to (set of) prompts, based on the dataset')
    parser.add_argument('--avg_annot_words', type=float, default=2,
        help='Average number of words in annotations (estimate)')
    parser.add_argument('--cost_per_1k_inp_tok', type=float, default=0.03,
        help='Cost of 1k input tokens for the specified API')  # 0.0015 for GPT 3.5
    parser.add_argument('--cost_per_1k_out_tok', type=float, default=0.06,
        help='Cost of 1k output tokens for the specified API')  # 0.002 for GPT 3.5
    parser.add_argument('--tok_scaling_factor', type=float, default=1.33,
        help='Average number of tokens per word')
    args = parser.parse_args()

    data_handler = utils.get_datahandler(args.dataset)
    i2p_funct = utils.get_inst2annot_prompt_func(args.inst_to_prompt_funct)

    annotator = Annotator(data_handler, i2p_funct, None, None, None)

    cost_est, num_tok, num_words, in_tok, out_tok = annotator.est_budget(args.avg_annot_words, args.tok_scaling_factor, args.cost_per_1k_inp_tok, args.cost_per_1k_out_tok)

    print(f'\n{args.dataset.upper()} ANNOTATION:\n')
    print(f'Estimated total cost: ${cost_est:0,.2f}')
    print(f'\t${args.cost_per_1k_out_tok:0,.2f}/{args.cost_per_1k_inp_tok:0,.2f} per 1K input/output tokens')
    print(f'\t@ {num_tok} Tokens ({in_tok}/{out_tok} in/out), {num_words} Words')
    print()


if __name__ == '__main__':
    main()
