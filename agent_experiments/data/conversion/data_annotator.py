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
        
    def annotate(self):
        f = open(self.out_file, 'w')
        for inst in self.dataset.instance_generator():
            annotations = self.annotate_instance(inst)
            out_line = self.output_formatter(inst, annotations)
            f.write(out_line)

        f.close()
