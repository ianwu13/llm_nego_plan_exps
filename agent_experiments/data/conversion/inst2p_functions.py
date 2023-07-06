"""
Functions which convert instances from dataset handlers into a set of annotation prompts for llms
"""


def example_inst2p_func(inst):  # Just for casino dataset, returns "annotate this: {utterance}"
    # print(inst)
    # print(type(inst))
    return [f"annotate this: {chat_item['text']}" for chat_item in inst['chat_logs']]

def format_prompt(str):
        prompt_str = "Predict the annotation for the last utterance by following the similar format as provided. "
        # format the utterance
        str = "utterance: " + str + "<eos> " + "annotation: "
        str = prompt_str + str
        return str

# split utterance seperately
def utters_split_seperate(line):
    # without the final selection
    utters_list = []
    for i in range (0, len(line.split("<eos>"))):
        each = line.split("<eos>")[i]
        each = format_prompt(each)
        utters_list.append(each)
    return utters_list

def demo_dnd(inst):
    # extract utterances
    dialogue_str = inst['dialogue']
    prompt_list = utters_split_seperate(dialogue_str )
    return prompt_list


def demo_casino(inst):
    # print(inst)
    prompt_list = []
    for each in inst['chat_logs']:
        prompt_intro = "annotate this : "
        prompt = prompt_intro + f"{each['id']}: {each['text']}"
        prompt_list.append(prompt)
    # print(prompt_list)
    return prompt_list


# ZORA UTILS
# assume read file methods are handle outside, and the input for the function is a string.
class i2p_functions():
    def __init__(self, input_file, output_file):
        self.input = input_file
        self.output = output_file

    def extract(self, str, tag):
        sub1 = "<" + tag + ">"
        sub2 = "</"+ tag + ">"
        
        idx1 = str.index(sub1)
        idx2 = str.index(sub2)

        output = str[idx1 + len(sub1) + 1: idx2]
        return output

    # # split utterance seperately
    # def utters_split_seperate(self, line):
    #     line = self.extract(line, "dialogue")
    #     utters_list = []
    #     for i in range (0, len(line.split("<eos>"))):
    #         each = line.split("<eos>")[i]
    #         each = self.format_prompt(each)
    #         utters_list.append(each)
    #     return utters_list

    # def utters_split_cumulative(self, line):
    #     line = self.extract(line, "dialogue")
    #     utters_list = []
    #     utters_list.append(self.format_prompt(line.split("<eos>")[0]))
    #     for i in range (1, len(line.split("<eos>"))):
    #         temp = line.split("<eos>")[i]
    #         each = utters_list[i-1] + temp
    #         each = self.format_prompt(each)
    #         utters_list.append(each)
    #     return utters_list

    # def format_prompt(self, str):
    #     prompt_str = "Predict the annotation for the last utterance by following the similar format as provided. "
    #     # format the utterance
    #     str = "utterance: " + str + "<eos> " + "annotation: "
    #     str = prompt_str + str
    #     return str

    def write_output(self, prompt_list, output_file_name):
        f = open(output_file_name, 'a')
        for each in prompt_list:
            f.write(each + '\n')
        f.close()

    def generate_prompt(self, func):
        file = open(self.input, 'r')
        lines = file.readlines()
        output_file_name = self.get_output_file_name(self.output)
        for each_line in lines:
            each_line = each_line.strip()

            if func == 'sep':
                prompt_sep_list = self.utters_split_seperate(each_line)
                self.write_output(prompt_sep_list, output_file_name)

            # by default the promp generation is based on cummulative utterance.
            else:
                prompt_cum_list = self.utters_split_cumulative(each_line)
                self.write_output(prompt_cum_list, output_file_name)

        print("Generate prompt done")
        file.close()

    def get_output_file_name(self, func):
        file_str = func + "_" + self.output
        return file_str
