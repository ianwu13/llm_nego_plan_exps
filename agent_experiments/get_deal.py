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
        each_prompt = [{'role': 'system', 'content': 'You are are assisting the user to detect the final deal of dividing 3 units each of firewood, water, and food in a negotiation diglogue. You should get final deal in this format "Alice: firewood=X water=X food=X Bob: firewood=X water=X food=X" and fill X with corresponding numbers from conversation.'}, 
            {'role': 'user', 'content': f'What is final deal for the conversation? {conv}'}]
        outs = api.get_chat_completions_out([each_prompt])
        final_deal = outs[0]
        # print(len(final_deal.split()))
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
    input_dir = 'storage/convo_jsons_for_deal_detection_testing'
    out_dir = 'storage/convo_jsons_for_deal_detection_testing'+'/get_final_deal'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            get_final_deal(filename, input_dir, out_dir)
        print("Done with file " + filename)


def main():
    get_all_deal()

if __name__ == "__main__":
    main()