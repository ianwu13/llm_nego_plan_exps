class Annotator():

    def __init__(self, dataset, inst2promp_funct, llm_api, output_formatter, out_file, failed_calls_file='failed_calls.txt'):
        self.dataset = dataset
        self.inst2promp_funct = inst2promp_funct
        self.llm_api = llm_api
        self.output_formatter = output_formatter
        self.out_file = out_file
        self.failed_calls_file = failed_calls_file

    def est_budget(avg_annot_words, tok_scaling_factor, cost_per_1k_tok):
        num_words = 0

        for split in self.dataset.splits:
            for dialogue in self.dataset.instance_generator(split):
                prompts = self.inst2promp_funct(dialogue)

                for p in prompts:
                    if isinstance(p, str):  # Completions Prompt
                        num_words += len(p)
                    elif isinstance(p, list):  # Chat Prompt
                        for msg in p:
                            num_words += len(msg['content'])

                # Account for returned tokens
                num_words += len(prompts) * avg_annot_words

        num_tok = num_words * tok_scaling_factor
        cost_est = cost_per_1k_tok * (num_tok / 1000)

        return cost_est, num_tok, num_words

    def annotate_instance(self, inst):
        prompts = self.inst2promp_funct(inst)
        annotations = self.llm_api.get_model_outputs(prompts)
        return annotations

    def annotate_split(self, outfile, split='train'):
        f = open(outfile, 'w')
        # for inst in self.dataset.instance_generator(split):
        for inst in self.dataset.get_instances(split=split, n=3):  # TODO: For testing so not too many api calls
            annotations = self.annotate_instance(inst)
            out_line = self.output_formatter(inst, annotations)
            f.write(out_line)
        f.close()

        # Write failed calls to file
        assert self.failed_calls_file.count('.') == 1
        fc_file_path = self.failed_calls_file.replace('.', f'_{split}')
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
