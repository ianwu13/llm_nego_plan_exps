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
    parser.add_argument('--start_index', type=int, default=0,
        help='Sample index of dataset to start annotating at')
    parser.add_argument('--inst_to_prompt_funct', type=str, default='example',
        help='function to convert instance (set of utterances) to (set of) prompts, based on the dataset')
    parser.add_argument('--annot_method', type=str, default='llm',
        help='Annotation method (llm or regex parser)')    
    parser.add_argument('--llm_api', type=str, default=None,
        help='llm api to be used in annotation')
    parser.add_argument('--llm_api_key', type=str, default=None,
        help='Key to be used when calling provided API')
    parser.add_argument('--postprocess', action='store_true', default=False,
        help='Apply postprocessing to annotations')
    parser.add_argument('--output_formatter', type=str, default='example',
        help='function to convert set of instance annotations to a string (line) for the output file')
    parser.add_argument('--output_file', type=str,
        help='destination for output file')
    parser.add_argument('--failed_calls_file', type=str,
        help='destination file for failed LLM API calls')
    args = parser.parse_args()

    data_handler = utils.get_datahandler(args.dataset)
    i2p_funct = utils.get_inst2annot_prompt_func(args.inst_to_prompt_funct)
    if args.annot_method == 'llm':
        annot_api = utils.get_llm_api(args.llm_api, args.llm_api_key)
    else:
        raise NotImplementedError("only llm annotation is currently implemented")
    output_formatter = utils.get_annot_out_formatter_func(args.output_formatter)

    annotator = Annotator(data_handler, i2p_funct, annot_api, output_formatter, args.output_file, args)

    annotator.annotate()

    print("Annotation all done.")


if __name__ == '__main__':
    main()
