"""
Annotate data using LLM apis
"""

import argparse
import pdb
from tqdm import tqdm
import json
import utils


class Converter():

    def __init__(self, dataset, annot_file, output_formatter, out_file):
        self.dataset = dataset
        self.annots = json.load(open(annot_file, 'r'))
        self.n = len(self.annots)
        self.output_formatter = output_formatter
        self.out_file = out_file
        
    def convert(self):
        f = open(self.out_file, 'w')
        print(f'Converting')
        for a_set, inst in zip(self.annots, self.dataset.get_instances(split='train', n=self.n)):
            annotations = [a[1] if isinstance(a[1], str) else ' '.join(a[1]) for a in a_set]
            annotations = [(a+' <eos>' if '<selection>' not in a else a) for a in annotations]
            out_line = self.output_formatter(inst, annotations)
            f.write(out_line)
        f.close()


def main():
    parser = argparse.ArgumentParser(description='script to annotate data')
    parser.add_argument('--dataset', type=str, choices=['dnd','casino'],
        help='Dataset handler ID')
    parser.add_argument('--annot_file', type=str, default=None,
        help='destination for validation file')
    parser.add_argument('--output_formatter', type=str, default=None,
        help='function to convert set of instance annotations to a string (line) for the output file')
    parser.add_argument('--output_file', type=str,
        help='destination for output file')
    args = parser.parse_args()

    data_handler = utils.get_datahandler(args.dataset)
    out_formatter = utils.get_annot_out_formatter_func(args.output_formatter)

    converter = Converter(data_handler, args.annot_file, out_formatter, args.output_file)

    converter.convert()

    print("Conversion all done.")


if __name__ == '__main__':
    main()

# python3 conv_e2e_format.py --dataset dnd --annot_file data/annot_val_sets/dnd_valset.json --output_formatter dnd_lstrip_annotation --output_file data/annot_val_sets/e2e_dnd_valset.txt
# python3 conv_e2e_format.py --dataset casino --annot_file data/annot_val_sets/casino_dndform_valset.json --output_formatter base_casino --output_file data/annot_val_sets/e2e_casino_dndform_valset.txt
# python3 conv_e2e_format.py --dataset casino --annot_file data/annot_val_sets/casino_customform_valset.json --output_formatter base_casino --output_file data/annot_val_sets/e2e_casino_customform_valset.txt
