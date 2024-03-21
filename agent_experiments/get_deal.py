from lang_models.llm_apis.open_ai import OpenAI_Api
import json
import os

api = OpenAI_Api('gpt-4', api_key="")

def get_final_deal(filename, input_dir, output_dir):
    count = 1
    f = open(os.path.join(input_dir, filename),"r")
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
            # print(len(final_deal.split()))
            each['final_deal'] = final_deal
        each['Conversation'] = count
        count += 1

    with open(os.path.join(output_dir, filename), "w") as outfile: 
        json.dump(conversations, outfile, indent=4)

def get_all_deal():
    input_dir = 'storage/convo_jsons_for_deal_detection_testing/new_json'
    out_dir = 'storage/convo_jsons_for_deal_detection_testing/new_deal'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            get_final_deal(filename, input_dir, out_dir)
        print("Done with file " + filename)

def tagged(deal_string):
    deal = deal_string.split(" ")
    if len(deal) == 8:
            firewood = float(deal[1].split("=")[1]) + float(deal[5].split("=")[1])
            water = float(deal[2].split("=")[1]) + float(deal[6].split("=")[1])
            food = float(deal[3].split("=")[1]) + float(deal[7].split("=")[1])
            # print(f"food: {food}; water: {water}; firewood: {firewood}")
            if firewood == 0 and water == 0 and food == 0:
                return "valid but disagree"
            
            elif food > 3.0 or water > 3.0 or firewood > 3.0:
                return "exceed"
            
            elif food < 3.0 or water < 3.0 or firewood < 3.0:
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
            tagged_deal = tagged(deal_string)
            summary[tagged_deal] += 1
            # print(tagged_deal)
            conv["is_valid"] = tagged_deal
            if "15" in deal_string or "1.5" in deal_string:
                conv["split"] = True
                summary["contains split"] += 1
            else:
                conv["split"] = False
        f.seek(0)  # rewind
        json.dump(all_convs, f, indent=4)
        f.truncate()

        return summary

    # json.dump(all_convs, input_dir+filename, indent=4 )



def main():
    # get_all_deal()
    
    input_dir = 'storage/convo_jsons_for_deal_detection_testing/new_deal'

    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            summary = classify(input_dir, filename)
            print(filename)
            print(str(summary)+"\n")


if __name__ == "__main__":
    main()