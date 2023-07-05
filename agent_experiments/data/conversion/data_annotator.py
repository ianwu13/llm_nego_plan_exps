from llm_apis import OpenAI_Api
from data.conversion.i2p_functions import i2p_functions

class Annotator():

    def __init__(self, dataset, api, input_file, output_file, i2p_method, prompt_method):
        self.dataset = dataset
        self.annotate_api = api
        self.input_file = input_file
        self.output_file = output_file
        self.i2p_method = i2p_method,
        self.prompt_method = prompt_method
        # self.annotate_api = generic api

    def annotate_each_line(self, prompt_file_name):
        file = open(prompt_file_name, 'r')

        annotated_file = 'open_ai' + self.prompt_method + 'annotated_' + prompt_file_name
        output_file = open(annotated_file, 'a')

        for each in file:
            output_file.write(each + '\n')   

            if self.prompt_method == 'chat_bot':
                generated_annotation = self.annotate_api.chat_bot(each, annotated_file)
                output_file.write("Result from chat_bot from OPEN_AI" + '\n')
                output_file.write(generated_annotation + '\n')
            else:
                generated_annotation = self.annotate_api.text_completion(each, annotated_file)
                output_file.write("Result from text_completion from OPEN_AI" + '\n')
                output_file.write(generated_annotation + '\n')

            output_file.write('---'*10 + '\n')

        output_file.close()
        file.close()
        

    def annotate(self):
        # generate prompt
        i2p_instance = i2p_functions(self.input_file, self.output_file)
        print(i2p_instance.output)
        print("generate prompt done")

        # argument choice from 'sep','cum'
        i2p_instance.generate_prompt(self.i2p_method)
        prompt_file_name = i2p_instance.get_output_file_name(self.i2p_method[0])
        self.annotate_each_line(prompt_file_name)
        print("annotation done")
