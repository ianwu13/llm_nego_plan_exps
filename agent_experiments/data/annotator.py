from tqdm import tqdm
import json

from simple_utils import remove_prefix


class Annotator():

    def __init__(self, dataset, inst2promp_funct, llm_api, output_formatter, out_file, args):
        self.dataset = dataset
        self.inst2promp_funct = inst2promp_funct
        self.llm_api = llm_api
        self.output_formatter = output_formatter
        self.out_file = out_file

        self.start_index = args.start_index
        self.failed_calls_file = args.failed_calls_file

        if hasattr(args, 'validation_file'):
            self.validation_file = args.validation_file


    def evaluate(self):
        assert self.validation_file, 'Must provide a validation file to compare against'

        val_set = json.load(open(self.validation_file, 'r'))
        n_val = len(val_set)

        total_count = 0
        propose_count = 0
        propost_correct = 0
        ema_sum = 0  # Exact match
        partial_math_sum = 0  # Some union
        subset_match_sum = 0  # number where pred is subset of true labels
        inverse_subset_match_sum = 0  # number where true is subset of pred labels
        no_match_sum = 0  # No matching between pred and true

        for inst, val_inst in zip(self.dataset.get_instances(split='train', n=n_val), val_set):
            tru_labels = [set([u[1]] if isinstance(u[1], str) else u[1]) for u in val_inst]
            pred_labels = [set([remove_prefix(remove_prefix(a, 'the annotation for this utterance is'), 'annotation ') for a in ann.split(', ')]) for ann in self.annotate_instance(inst)]

            # Write annotations to file if needed
            if self.output_formatter:
                f = open(self.out_file, 'a')
                out_line = self.output_formatter(inst, [' '.join(p) for p in pred_labels])
                f.write(out_line)
                f.close()

            for t, p in zip(tru_labels, pred_labels):
                if t == '<selection>':
                    continue
                
                total_count += 1
                ema_sum += 1 if t == p else 0  # Exact match
                for a in p:
                    if a in t:
                        partial_math_sum += 1  # Some union
                        break
                for i in t:
                    if 'propose' in i:
                        propose_count += 1
                        if i in a:
                            propost_correct += 1
                subset_match_sum += 1 if p.issubset(t) else 0  # number where pred is subset of true labels
                inverse_subset_match_sum += 1 if t.issubset(p) else 0  # number where true is subset of pred labels
                no_match_sum += 1 if not(p & t) else 0  # No matching between pred and true
            
        print(f'Total Utterances: {total_count}')
        print(f'Exact match Ratio: {ema_sum / total_count}')
        print(f'Some union Ratio: {partial_math_sum / total_count}')
        print(f'Number where pred is subset of true labels Ratio: {subset_match_sum / total_count}')
        print(f'Number where true is subset of pred labels Ratio: {inverse_subset_match_sum / total_count}')
        print(f'No matching between pred and true Ratio: {no_match_sum / total_count}')
        print(f'Propose correct ratio: {propost_correct/propose_count}')


    def est_budget(self, avg_annot_words, tok_scaling_factor, cost_per_1k_inp_tok, cost_per_1k_out_tok):
        num_in_words = 0
        num_out_words = 0

        for split in self.dataset.splits:
            for dialogue in self.dataset.instance_generator(split):
                prompts = self.inst2promp_funct(dialogue)

                for p in prompts:
                    if isinstance(p, str):  # Completions Prompt
                        num_in_words += len(p)
                    elif isinstance(p, list):  # Chat Prompt
                        for msg in p:
                            num_in_words += len(msg['content'])

                # Account for returned tokens
                num_out_words += len(prompts) * avg_annot_words

        num_in_tok = num_in_words * tok_scaling_factor
        in_cost_est = cost_per_1k_inp_tok * (num_in_tok / 1000)

        num_out_tok = num_out_words * tok_scaling_factor
        out_cost_est = cost_per_1k_out_tok * (num_out_tok / 1000)

        cost_est = in_cost_est + out_cost_est
        num_tok = num_in_tok + num_out_tok
        num_words = num_in_words + num_out_tok

        return cost_est, num_tok, num_words, num_in_tok, num_out_tok

    def annotate_instance(self, inst):
        prompts = self.inst2promp_funct(inst)
        annotations = self.llm_api.get_model_outputs(prompts)
        return annotations

    def annotate_split(self, outfile, split='train'):
        f = open(outfile, 'w')
        print(f'Annotating {split}')
        # for inst in tqdm(self.dataset.get_instances(split=split, n=3)):  # For testing so not too many api calls
        cur_ind = 0
        for inst in tqdm(self.dataset.instance_generator(split)):
            if not cur_ind >= self.start_index:
                cur_ind += 1
                continue

            annotations = self.annotate_instance(inst)
            out_line = self.output_formatter(inst, annotations)
            f.write(out_line)
        f.close()

        # Write failed calls to file
        sp = self.failed_calls_file.split('.')
        sp[-2] += f'_{split}'
        fc_file_path = '.'.join(sp)
        f = open(fc_file_path, 'w')
        for call in self.llm_api.failed_calls:
            f.write(json.dumps(call) + '\n')
        f.close()
        self.llm_api.failed_calls = []
        
    def annotate(self, split=None):
        if split is None:
            for sp in self.dataset.splits:
                sp_file = f'_{sp}.'.join(self.out_file.rsplit('.', 1))
                self.annotate_split(sp_file, sp)
        else:
            self.annotate_split(self.out_file, split)
