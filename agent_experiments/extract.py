import json
import os

def extract(input_dir, filename, output_dir, outfilename):
    all_dialgue = []
    temp = []
    start_flag = False
    count = 0
    with open(os.path.join(input_dir, filename), 'r') as f:
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
        temp = {"alice_pref":each[0],
                "bob_pref": each[1],
                "convo": each[2:cut]}
        json_data.append(temp)
    
    with open(os.path.join(output_dir, outfilename), 'w') as f:
        f.write(json.dumps(json_data, indent=4))

def main():
    input_dir = 'llm_negotiation/llm_nego_plan_exps/agent_experiments/storage/logs/gpt-4/casino/selfplay'
    out_dir = 'storage/convo_jsons_for_deal_detection_testing/new_final_deal'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for filename in os.listdir(input_dir):
        if filename.endswith('.log'):
            outfilename = filename.split(".")[0]+".json"
            extract(input_dir, filename, out_dir, outfilename)
        print("Done with file " + filename)

if __name__ == "__main__":
    main()