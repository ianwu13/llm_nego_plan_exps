import itertools
import json
import sys

agents = ["llm_no", "llm_self", "rl_fair",  "rl_self", "rl_ss"]
strategy_type = ["generic"]

casino_rl_weight_file = {"rl_fair": "models/fd_jan24_fixed/jan24_casino_custform_rl_fair_4ep_fixed_rw_combine50_50.pt",        
                  "rl_self": "models/fd_jan24_fixed/jan24_casino_custform_rl_selfish_4ep_fixed_rw_own_points.pt",
                  "rl_ss": "models/fd_jan24_fixed/jan24_casino_custform_rl_selfish_v_selfish_4ep_fixed_rw_own_points.pt"}

dnd_rl_weight_file = {"rl_fair": "models/dnd_rl_fair_4ep_rw_combine50_50.pt",        
                  "rl_self": "models/dnd_rl_selfish_4ep_rw_own_points.pt",
                  "rl_ss": "models/dnd_supervised_30ep.pt"}

selfplay_template = {
    "--dataset" : None,
    "--alice_type" : None,
    # "--alice_template_gen" : "False",
    "--alice_strategy" : None,
    "--bob_type" : None,
    # "--bob_template_gen" : "False",
    "--bob_strategy" : None,
    "--llm_api" : None,
    "--llm_api_key" : None,
    "--utt2act_prompt_func" : None,
    "--act2utt_prompt_func" : None,
    "--llm_response_prompt_func_alice" : None,
    "--llm_response_prompt_func_bob" : None,
    "--llm_choice_prompt_func" : None,
    "--alice_model_file" : None,
    "--bob_model_file": None,
    "--corpus_source": None,
    "--max_turns": 20,
    "--context_file": None,
    "--ref_text": None,
    "--log_file": None,
}

def set_dataset(dataset_name, gpt_version, api_key):
    selfplay_template["--llm_api"] = gpt_version
    selfplay_template["--llm_api_key"] = api_key

    if dataset_name == "casino":
        selfplay_template["--dataset"] = "casino"
        selfplay_template["--context_file"] = "data/raw_datasets/dummy/casino_ctx.txt"
        selfplay_template["--ref_text"] = "data/raw_datasets/dummy/casino_ref.txt"
        selfplay_template["--llm_choice_prompt_func"] = "choice_slagent_chatcomp_thirdperson_casino"
        selfplay_template["--utt2act_prompt_func"] = "reduced_casino_cust_format"
        selfplay_template["--act2utt_prompt_func"] = "casino_a2u_prompt"
        selfplay_template["--corpus_source"] = "data/fd_r2_jan_2024_fixed/train.txt"
    
    elif dataset_name == "dnd":
        selfplay_template["--dataset"] = "dnd"
        selfplay_template["--context_file"] = "data/raw_datasets/dummy/dnd_ctx.txt"
        selfplay_template["--ref_text"] = "data/raw_datasets/dummy/dnd_ref.txt"
        selfplay_template["--llm_choice_prompt_func"] = "choice_slagent_chatcomp_thirdperson_dnd"
        selfplay_template["--utt2act_prompt_func"] = "final_utt2act_dnd"
        selfplay_template["--act2utt_prompt_func"] = "dnd_a2u_prompt"
        selfplay_template["--corpus_source"] = "data/final_datasets/R1_dnd/train.txt"

    else:
        raise Exception("Undefined dataset name")

def set_agent(dataset, agent_name, strategy_type, side_name):
    if dataset == "casino":
        if agent_name == "llm_no":
            selfplay_template[f"--{side_name}_type"] = "llm_no_planning"
            selfplay_template[f"--{side_name}_strategy"] = strategy_type
            selfplay_template[f"--llm_response_prompt_func_{side_name}"] = "dia_resp_slagent_chatcomp_casino" 

        elif agent_name == "llm_self":
            selfplay_template[f"--{side_name}_type"] = "llm_self_planning"
            selfplay_template[f"--{side_name}_strategy"] = strategy_type
            selfplay_template[f"--llm_response_prompt_func_{side_name}"] = "act_act_chatcomp_casino_cust_form"
        
        # RL_planning
        else: 
            selfplay_template[f"--{side_name}_type"] = "llm_rl_planning"
            selfplay_template[f"--{side_name}_strategy"] = strategy_type
            selfplay_template[f"--{side_name}_model_file"] = casino_rl_weight_file[agent_name]

    elif dataset == "dnd":
        if agent_name == "llm_no":
            selfplay_template[f"--{side_name}_type"] = "llm_no_planning"
            selfplay_template[f"--{side_name}_strategy"] = strategy_type
            selfplay_template[f"--llm_response_prompt_func_{side_name}"] = "dia_resp_slagent_chatcomp_dnd" 

        elif agent_name == "llm_self":
            selfplay_template[f"--{side_name}_type"] = "llm_self_planning"
            selfplay_template[f"--{side_name}_strategy"] = strategy_type
            selfplay_template[f"--llm_response_prompt_func_{side_name}"] = "act_act_chatcomp_dnd"
        
        # RL_planning
        else: 
            selfplay_template[f"--{side_name}_type"] = "llm_rl_planning"
            selfplay_template[f"--{side_name}_strategy"] = strategy_type
            selfplay_template[f"--{side_name}_model_file"] = dnd_rl_weight_file[agent_name]

    else:
        raise Exception("Undefined dataset name")

def clean_commd():
    remove_char = ["'", ",", ":", "{", "}"]
    commd = str(selfplay_template)
    for each in remove_char:
        commd = commd.replace(each, "")
    return f"python3 do_selfplay.py {commd}"

def create_selfplay_commd(agent_list, strategy_list, dataset_name, gpt_version, api_key, f, commd_list):
    set_dataset(dataset_name, gpt_version, api_key)
    agent_pair = list(itertools.product(agent_list, strategy_list))

    count = 1
    for each_alice in agent_pair:
        for each_bob in agent_pair:
            each_commd = {}
            set_agent(dataset_name, each_alice[0], each_alice[1], "alice")
            set_agent(dataset_name, each_bob[0], each_bob[1], "bob")
            alice_name = each_alice[1] + "_" + each_alice[0]
            bob_name = each_bob[1] + "_" + each_bob[0]
            log_file_name = f"storage/logs/{gpt_version}/{dataset_name}/selfplay/{alice_name}_vs_{bob_name}.log"
            selfplay_template["--log_file"] = log_file_name
            commd = clean_commd()
            f.write(f"-------- Command {count} for {alice_name} vs {bob_name} in {dataset_name} ({gpt_version}) -------- \n\n")
            f.write(commd)
            f.write("\n\n")
            each_commd["order"] = count
            each_commd["agents"] = f"{alice_name} vs {bob_name}"
            each_commd["commd"] = commd
            commd_list.append(each_commd)
            count += 1

def main():
    args = sys.argv[1:]
    dataset = args[0] # "dnd" or "casino"
    api_key = "key_value"
    
    if len(args) > 1:
        api_key = args[1] # Fill with API KEY

    gpt_version = "gpt-4"

    f = open(f"commd_selfplay_{dataset}.md","w+")
    commd_list = []
    create_selfplay_commd(agents, strategy_type, dataset, gpt_version, api_key, f, commd_list)
    f.close()

    with open(f"commd_selfplay_{dataset}.json", 'w') as f:
        json.dump(commd_list, f, indent=4)

if __name__ == "__main__":
    main()