from llm_apis import OpenAI_Api

class Annotator():

    def __init__(self, dataset, api, output_file):
        self.dataset = dataset
        self.annotate_api = api
        self.output_file = output_file
        # self.annotate_api = generic api


    def annotate_line(self):
        f = open(self.input_file, "r")
        self.annotate_api.get_model_outputs(f.readlines())
        

    def annotate(self):
        self.annotate_line()
