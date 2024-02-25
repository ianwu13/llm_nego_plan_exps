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
    parser.add_argument('--llm_api', type=str, default=None,
        help='llm api to be used in annotation')
    parser.add_argument('--llm_api_key', type=str, default=None,
        help='Key to be used when calling provided API')
    parser.add_argument('--postprocess', action='store_true', default=False,
        help='Apply postprocessing to annotations')
    parser.add_argument('--validation_file', type=str, default=None,
        help='destination for validation file')

    parser.add_argument('--output_formatter', type=str, default=None,
        help='function to convert set of instance annotations to a string (line) for the output file')
    parser.add_argument('--output_file', type=str, default=None,
        help='destination for output file')
    args = parser.parse_args()
    
    # Handle unused arg for annotator init
    args.start_index = 0  
    args.failed_calls_file = None

    data_handler = utils.get_datahandler(args.dataset)
    i2p_funct = utils.get_inst2annot_prompt_func(args.inst_to_prompt_funct)
    annot_api = utils.get_llm_api(args.llm_api, args.llm_api_key)
    if args.output_formatter:
        out_formatter = utils.get_annot_out_formatter_func(args.output_formatter)
    else:
        out_formatter = None

    annotator = Annotator(data_handler, i2p_funct, annot_api, out_formatter, args.output_file, args)

    annotator.evaluate()

    print("Evaluation all done.")


if __name__ == '__main__':
    main()


# python3 eval_annot_functions.py --dataset casino --inst_to_prompt_funct finalized_casino_cust_format --llm_api gpt-3.5-turbo-0613 --llm_api_key FILL --validation_file data/annot_val_sets/casino_customform_valset.json
# python3 eval_annot_functions.py --dataset dnd --inst_to_prompt_funct finalized_dnd --llm_api gpt-3.5-turbo-0613 --llm_api_key FILL --validation_file data/annot_val_sets/dnd_valset.json