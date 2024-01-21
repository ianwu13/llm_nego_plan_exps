import json
import sys
dnd_items = ['books', 'hats', 'balls']
casino_items = ['firewood', 'water', 'food']
dnd_label = ["smalltalk", 'propose', 'inquire', 'insist', "agree", "disagree", "unknown"]
casino_label = ["noneed", "undervalue", "expresspreference", "elicitpreference", "vouchfairness",
             "empathycoordination","smalltalk", 'propose', 'inquire', 'insist', "agree", "disagree", "unknown"]
def remove_space(annot_list):
    for i in range(0, len(annot_list)):
        each = annot_list[i]
        each = each.replace("no need", "noneed")
        each = each.replace("under value", "undervalue")
        each = each.replace("express preference", "expresspreference")
        each = each.replace("elicit preference", "elicitpreference")
        each = each.replace("vouch fairness", "vouchfairness")
        each = each.replace("empathy coordination", "empathycoordination")
        each = each.replace("small talk", "smalltalk")
        annot_list[i] = each
    return annot_list

# processing each annotation
def process_annot(annot_list, item_list, label_list):
    annot_list = remove_space(annot_list)
    label_w_count = ['propose', 'insist']
    label_w_item = ['noneed', 'inquire','expresspreference', 'elicitpreference', 'undervalue']
    new_list = []
    propose_flag = False
    print("---") 
    for each in annot_list:
        # print("each label: " + each)
        remove_flag = False
        token_list = each.split()
        # print(len(token_list))
        # print("check first ++ " + token_list[0])
        if len(token_list) == 1:
            if token_list[0] in label_w_count: # propose/inquire/insist exist solely
                remove_flag = True
            elif token_list[0] not in label_list:
                remove_flag = True
            else:
                each = token_list[0]
        else: # len(token_list) > 1:
            if token_list[0] in label_w_count:
                new_label = token_list[0]
                count = 0
                for each_item in token_list[1:]: # item should with value
                        temp_index = each_item.find("=")
                        if count < 3:
                            if temp_index > 1 and each_item[:temp_index] in item_list:
                                new_label = new_label + " " + each_item
                                count += 1
                            else:
                                break
                if count == 0: # propose/inquiry/insist with no item  following
                     remove_flag = True
                else:
                    # print("new propose" + new_label)
                    each = new_label
                remaining = ' '.join(token_list[1:])
                annot_list.append(remaining)

            elif token_list[0] in label_w_item:
                new_label = token_list[0]
                next_item = token_list[1]
                if next_item in item_list:
                    new_label += " " + next_item
                elif "=" in next_item:
                    temp_index = next_item.find("=")
                    new_item = next_item[:temp_index]
                    new_label += " " + new_item
                else:
                    continue
                remaining = ' '.join(token_list[1:])
                annot_list.append(remaining)
                each = new_label

            elif token_list[0] in label_list:
                new_label = token_list[0]
                remaining = ' '.join(token_list[1:])
                annot_list.append(remaining)
                each = new_label
            else: # token_list[0] not in label_list:
                # print("not show " + token_list[0])
                remaining = ' '.join(token_list[1:])
                annot_list.append(remaining)
                remove_flag = True
            
        # print("remove flag " + str(remove_flag))
        if not remove_flag:
            new_list.append(each)
            if token_list[0] == 'propose':
                propose_flag = True

    if not new_list: # if new list is empty:
        new_list.append("unknown")
    print("---")   
    for each in new_list:
        print(each)
    print("+++") 

    # filter duplicate annotation:
    new_list = list(set(new_list))



    # filter preference express if propose present
    annot_str = ''
    if propose_flag:
        for each in new_list:
            if "expresspreference" not in each:
                annot_str += each + ' '
    else:
        annot_str = ' '.join(new_list)
    
    print(annot_str)
    print("=====") 

    # new_annot_str = ' '.join(annot_list)
    return annot_str


def process_conver(conv, item_list, label_list):
    new_conv = []
    # new_conv_chop = []
    for each_turn in conv:
        # each_turn[0] is utterance
        # each_turn[1] is annotation list with only one annotation in string
        print("Utterance: " + each_turn[0])
        fixed_annot = process_annot(each_turn[1], item_list, label_list)
        new_conv.append(fixed_annot)

    # new_conv_chop = [i for i in new_conv if i != "smalltalk" and i != "agree"] 
    return format(new_conv)

def format(conv):
    result = ''
    chop_result = ''
    label_list = ['YOU: ', 'THEM: ']
    agree_count = 0
    for i in range(0,len(conv)-1):
        # label with name laternatively
        format_annot = label_list[i%2] + conv[i] + ' <eos> '
        result += format_annot
        # Chop off beginning of conversations if utterance is only small-talk
        # i < 5 for presenting the begining of conv
        if i < 5 and conv[i] == 'smalltalk' or conv[i] == 'unknown' :
            continue
        # Chop off too many agrees at the end, only keep 2
        elif conv[i] == 'agree' and agree_count < 2:
            agree_count += 1
            chop_result += format_annot
        else:
            chop_result += format_annot

    result = '<dialogue> ' + result + ' \<dialogue>'
    chop_result = '<dialogue> ' + chop_result + ' \<dialogue>'
    return result, chop_result

# python3 postprocess.py input_file_name output_file_name datasetname(dnd or casino, default = dnd)
def main(argv):
    file_name = argv[0]
    out_file_name = argv[1]
    out_file_name_chop = 'chop_' + out_file_name
    # dataset = 'dnd'
    item_list = dnd_items
    label_list = dnd_label
    if argv[2] == 'casino':
        item_list = casino_items
        label_list = casino_label

    input_file = open(file_name, 'r')
    output_file = open(out_file_name, 'w')
    output_file_chop = open(out_file_name_chop, 'w')
    data = json.load(input_file)
    for index, each_conver in enumerate(data):
        print("CONVERSATION:" + str(index))
        conv1, conv2 = process_conver(each_conver, item_list, label_list)
        output_file.write(str(conv1) + '\n')
        output_file_chop.write(str(conv2) + '\n')
        # print(each_conversation)
    input_file.close()
    output_file.close()
    output_file_chop.close()
 
if __name__ == "__main__":
    main(sys.argv[1:])