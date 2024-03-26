import json
import os
import sys

def extract(filename, outfilename):
    all_dialgue = []
    temp = []
    start_flag = False
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            if "===" in line:
                if start_flag:
                    start_flag = False
                    count = 0
                    all_dialgue.append(temp)
                else:
                    start_flag = True
                    temp = []
            if "---" in line:
                count += 1
            if "---" not in line and "===" not in line and start_flag and count <= 1:
                temp.append(line)

    json_data = []
    for each in all_dialgue:
        cut = len(each)
        if "=" in each[-1]:
            cut = -1
        if "=" in each [-2]:
            cut = -2
        temp = {"alice_pref":each[0][:-1],
                "bob_pref": each[1][:-1],
                "convo": each[2:cut]}
        json_data.append(temp)
    
    with open(outfilename, 'w') as f:
        f.write(json.dumps(json_data, indent=4))
    print("Done with file " + filename)

def extract_all(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        if filename.endswith('.log'):
            outfilename = filename.split(".")[0]+".json"
            extract(os.path.join(input_dir, filename),os.path.join(output_dir, outfilename))

def main():
    args = sys.argv[1:]
    dataset = args[0] # "dnd" or "casino"
    input_dir = f'storage/logs/gpt-4/{dataset}/selfplay'
    output_dir = f'storage/extracted_conv/{dataset}/selfplay'
    extract_all(input_dir, output_dir)

    # if want to extract only one file
    # extract(f1, f2)

if __name__ == "__main__":
    main()