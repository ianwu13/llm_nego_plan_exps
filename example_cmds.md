# Example Commands

### Data Annotation

Demo annotate DND dataset
```
python3 annotate.py --dataset dnd --inst_to_prompt_funct demo_dnd --annot_method llm --llm_api dummy --output_formatter demo_dnd_outform --output_file data/raw_datasets/DEMO.txt
```

Demo annotate CaSiNo dataset
```
python3 annotate.py --dataset casino --inst_to_prompt_funct demo_casino --annot_method llm --llm_api dummy --output_formatter demo_casino_outform --output_file data/raw_datasets/DEMO.txt
```

### Selfplay

Selfplay, alice/bob as single-level llm models
```
python3 do_selfplay.py --alice_type llm_no_planning --bob_type llm_no_planning --llm_api dummy --llm_response_prompt_func example_dia_resp --llm_choice_prompt_func example_choice --context_file data/raw_datasets/dummies/ctx_example.txt --ref_text data/raw_datasets/dummies/ref_example.txt --log_file storage/logs/sp_slAgent_davinci003.log
```

Selfplay, alice/bob as dual-level llm models
```
python3 do_selfplay.py --alice_type llm_self_planning --bob_type llm_self_planning --llm_api dummy --utt2act_prompt_func example --act2utt_prompt_func example --llm_response_prompt_func example_dia_act_resp --llm_choice_prompt_func example_choice --context_file data/raw_datasets/dummies/ctx_example.txt --ref_text data/raw_datasets/dummies/ref_example.txt --log_file storage/logs/sp_dlAgentSelfPlanning_davinci003.log
```

Selfplay, alice/bob as dual-level llm models with RL planning module
```
python3 do_selfplay.py --alice_type llm_rl_planning --bob_type llm_rl_planning --llm_api dummy --alice_model_file models/sv_model_30ep_dndNegotiate.pt --bob_model_file models/sv_model_30ep_dndNegotiate.pt --utt2act_prompt_func example --act2utt_prompt_func example --llm_choice_prompt_func example_choice --context_file data/raw_datasets/dummies/ctx_example.txt --ref_text data/raw_datasets/dummies/ref_example.txt --corpus_source data/raw_datasets/dummies/ref_example.txt --log_file storage/logs/sp_dlAgentRLPlanning_davinci003.log
```

### Chat

Chat with AI as single-level llm agent
```
python3 do_chat.py --ai_type llm_no_planning --llm_api dummy --llm_response_prompt_func example_dia_resp --llm_choice_prompt_func example_choice --context_file data/raw_datasets/dummies/ctx_example.txt --ref_text data/raw_datasets/dummies/ref_example.txt --log_file storage/logs/chat_slAgent_davinci003.log
```

Chat with AI as dual-level llm model
```
python3 do_chat.py --ai_type llm_self_planning --llm_api dummy --utt2act_prompt_func example --act2utt_prompt_func example --llm_response_prompt_func example_dia_act_resp --llm_choice_prompt_func example_choice --context_file data/raw_datasets/dummies/ctx_example.txt --ref_text data/raw_datasets/dummies/ref_example.txt --log_file storage/logs/chat_dlAgentSelfPlanning_davinci003.log
```

Chat with AI as dual-level llm model with RL planning module
```
python3 do_chat.py --ai_type llm_rl_planning --llm_api dummy --model_file models/sv_model_30ep_dndNegotiate.pt --utt2act_prompt_func example --act2utt_prompt_func example --llm_response_prompt_func example_dia_act_resp --llm_choice_prompt_func example_choice --context_file data/raw_datasets/dummies/ctx_example.txt --ref_text data/raw_datasets/dummies/ref_example.txt --corpus_source data/raw_datasets/dummies/ref_example.txt --log_file storage/logs/chat_dlAgentRLPlanning_davinci003.log
```
