class Annotator():

    def __init__(self, dataset, inst2promp_funct, llm_api, output_formatter, out_file):
        self.dataset = dataset
        self.inst2promp_funct = inst2promp_funct
        self.llm_api = llm_api
        self.output_formatter = output_formatter
        self.out_file = out_file

    def annotate_instance(self, inst):
        prompts = self.inst2promp_funct(inst)
        annotations = self.llm_api.get_model_outputs(prompts)
        return annotations

    def annotate_split(self, outfile, split='train'):
        f = open(outfile, 'w')
        # for inst in self.dataset.instance_generator(split):
        for inst in self.dataset.get_instances(split=split, n=1):  # TODO: For testing so not too many api calls
            print(inst)
            annotations = self.annotate_instance(inst)
            out_line = self.output_formatter(inst, annotations)
            f.write(out_line)
        f.close()
        
    def annotate(self, split=None):
        if split is None:
            for sp in self.dataset.splits:
                sp_file = f'_{sp}.'.join(self.out_file.rsplit('.', 1))
                self.annotate_split(sp_file, sp)
        else:
            self.annotate_split(self.out_file, split)
