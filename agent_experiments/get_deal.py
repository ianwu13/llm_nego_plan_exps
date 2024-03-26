from lang_models.llm_apis.open_ai import OpenAI_Api
import json
import os
import sys

def get_casino_final_deal(api, filename, outfile):
    count = 1
    f = open(filename,"r")
    conversations = json.load(f)

    for each in conversations:
        conv = "".join(each["convo"])
        each_prompt = [{'role': 'system', 'content': 'You are are assisting the user to detect the final deal of dividing 3 units each of firewood, water, and food in a negotiation diglogue. You should get final deal in this format "Alice: firewood=X water=X food=X Bob: firewood=X water=X food=X" and fill X with corresponding numbers from conversation. If no deal reached in the end, fill all X with 0s.'}, 
            {'role': 'user', 'content': f'What is final deal for the conversation? {conv}'}]
        outs = api.get_chat_completions_out([each_prompt])
        final_deal = outs[0]
        print(len(final_deal.split()))
        if len(each["convo"]) >= 20:
            each['final_deal'] = "alice firewood=0 water=0 food=0 bob firewood=0 water=0 food=0"
        else:
            each['final_deal'] = final_deal
        each['Conversation'] = count
        count += 1

    with open(outfile, "w") as outfile: 
        json.dump(conversations, outfile, indent=4)

def get_dnd_final_deal(api, filename, outfile):
    count = 1
    f = open(filename,"r")
    conversations = json.load(f)

    for each in conversations:
        conv = "".join(each["convo"])
        counts = each["alice_pref"].split("count:")
        num_book = counts[1][0]
        num_hat = counts[2][0]
        num_ball = counts[3][0]

        each_prompt = [{'role': 'system', 'content': f'You are are assisting the user to detect the final deal of dividing {num_book} units of books,{num_hat} units of hats, and {num_ball} units of balls in a negotiation diglogue. You should get final deal in this format "Alice: book=X hat=X ball=X Bob: book=X hat=X ball=X" and fill X with corresponding numbers from conversation. If no deal reached in the end, fill all X with 0s.'}, 
            {'role': 'user', 'content': f'What is final deal for the conversation? {conv}'}]
        outs = api.get_chat_completions_out([each_prompt])
        final_deal = outs[0]
        print(len(final_deal.split()))
        if len(each["convo"]) >= 20:
            each['final_deal'] = "alice book=0 hat=0 ball=0 bob book=0 hat=0 ball=0"
        else:
            each['final_deal'] = final_deal
        each['Conversation'] = count
        count += 1

    with open(outfile, "w") as outfile: 
        json.dump(conversations, outfile, indent=4)

def get_all_deal(api, dataset, input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            if dataset == "casino":
                get_casino_final_deal(api, os.path.join(input_dir, filename), os.path.join(output_dir, filename))
            elif dataset == "dnd":
                get_dnd_final_deal(api, os.path.join(input_dir, filename), os.path.join(output_dir, filename))
            else:
                raise Exception("Undefined dataset name")
        print("Done with file " + filename)

def tagged(availables, deal_string):
    deal = deal_string.split(" ")
    if len(deal) == 8:
        item1 = float(deal[1].split("=")[1]) + float(deal[5].split("=")[1])
        item2 = float(deal[2].split("=")[1]) + float(deal[6].split("=")[1])
        item3 = float(deal[3].split("=")[1]) + float(deal[7].split("=")[1])

        if item1 == 0 and item2 == 0 and item3 == 0:
            return "valid but disagree"
        
        elif item1 > availables[0] or item2 > availables[1] or item3 > availables[2]:
            return "exceed"
        
        elif item1 < availables[0] or item2 < availables[1] or item3 < availables[2]:
            return "valid but not optimal"
        
        else:
            return "valid and agree"

    else:
        return "wrong deal format"

def classify(input_dir, filename):
    summary = {"valid and agree": 0,
                "valid but disagree": 0,
                "excceed": 0,
                "valid but not optimal": 0,
                "wrong deal format": 0,
                "contains split": 0}
    
    with open(os.path.join(input_dir, filename),"r+") as f:
        all_convs = json.load(f)
        for conv in all_convs:
            deal_string = conv["final_deal"]
            counts = conv["alice_pref"].split("count:")
            availables = [float(counts[1][0]), float(counts[2][0]), float(counts[3][0])]
            tagged_deal = tagged(availables , deal_string)
            summary[tagged_deal] += 1
            # print(tagged_deal)
            conv["is_valid"] = tagged_deal
            if "15" in deal_string or "1.5" in deal_string or "." in deal_string:
                conv["split"] = True
                summary["contains split"] += 1
            else:
                conv["split"] = False
        f.seek(0)  # rewind
        json.dump(all_convs, f, indent=4)
        f.truncate()

        return summary

def get_stats(input_dir):
    all_stats = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            summary = classify(input_dir, filename)
            stats = {'filename':filename,
                     'stats': summary}
            all_stats.append(stats)
            print(filename)
            print(str(summary)+"\n")
    out_file = open(os.path.join(input_dir, "stats.json"), "w") 
    json.dump(all_stats, out_file, indent=4 )

def main():
    args = sys.argv[1:]
    dataset = args[0] # "dnd" or "casino"
    user_api_key = args[1]
    api = OpenAI_Api('gpt-4', api_key=user_api_key)
    input_dir = f'storage/extracted_conv/{dataset}/selfplay'
    output_dir = f'storage/convo_jsons_for_deal_detection_testing/{dataset}/selfplay'
    
    # get_all_deal(api, dataset, input_dir, output_dir)
    get_stats(output_dir)

if __name__ == "__main__":
    main()