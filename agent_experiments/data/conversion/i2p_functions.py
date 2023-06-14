"""
Functions which convert instances from dataset handlers into a set of annotation prompts for llms
"""


def example_i2p_func(inst):  # Just for casino dataset, returns "annotate this: {utterance}"
    return [f"annotate this: {chat_item['text']}" for chat_item in inst['chat_logs']]


# TODO: ZORA UTILS
# assume read file methods are handle outside, and the input for the function is a string.
def extract(str,tag):
    sub1 = "<" + tag + ">"
    sub2 = "</"+ tag + ">"
    
    idx1 = str.index(sub1)
    idx2 = str.index(sub2)

    output = str[idx1 + len(sub1) + 1: idx2]
    return output

# split utterance seperately
def utters_split_seperate(line):
    line = extract(line, "dialogue")
    utters_list = []
    for i in range (0, len(line.split("<eos>"))):
        each = line.split("<eos>")[i]
        each = format_prompt(each)
        utters_list.append(each)
    return utters_list

def utters_split_cumulative(line):
    line = extract(line, "dialogue")
    utters_list = []
    utters_list.append(format_prompt(line.split("<eos>")[0]))
    for i in range (1, len(line.split("<eos>"))):
        temp = line.split("<eos>")[i]
        each = utters_list[i-1] + temp
        each = format_prompt(each)
        utters_list.append(each)
    return utters_list

def format_prompt(str):
    prompt_str = "Predict the annotation for the last utterance by following the similar format as provided. "
    # format the utterance
    str = "utterance: " + str + "<eos> " + "annotation: "
    str = prompt_str + str
    return str

def write_output(prompt_list, output_file):
    f = open(output_file, 'a')
    for each in prompt_list:
        f.write(each + '\n')
    f.close()

def main():
    file = open('data.txt', 'r')
    lines = file.readlines()

    for each_line in lines:
        each_line = each_line.strip()
        prompt_sep_list = utters_split_seperate(each_line)
        write_output(prompt_sep_list,'result_sep.txt')

        prompt_cum_list = utters_split_cumulative(each_line)
        write_output(prompt_cum_list,'result_cum.txt')
    print("done")
        

if __name__ == "__main__":
    main()
