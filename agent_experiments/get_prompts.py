"""
Annotate data using LLM apis
"""

import argparse
import json

import utils


def main():
    parser = argparse.ArgumentParser(description='script to annotate data')
    parser.add_argument('--dataset', type=str, choices=['dnd','casino'],
        help='Dataset handler ID')
    parser.add_argument('--num_inst', type=int,
        help='Number of instances to get prompts for')
    parser.add_argument('--inst_to_prompt_funct', type=str, default='example',
        help='function to convert instance (set of utterances) to (set of) prompts, based on the dataset')
    parser.add_argument('--output_file', type=str,
        help='destination for output file')
    args = parser.parse_args()

    data_handler = utils.get_datahandler(args.dataset)
    i2p_funct = utils.get_inst2annot_prompt_func(args.inst_to_prompt_funct)

    prompt_list = []
    for inst in data_handler.get_instances(split='train', n=args.num_inst):
        prompt_list.append(i2p_funct(inst))

    with open(args.output_file, 'w') as f:
        f.write(json.dumps(prompt_list))

    print("Done.")


if __name__ == '__main__':
    main()
