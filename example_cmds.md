# Example Commands

### Data Annotation

```
python3 annotate.py --dataset casino --inst_to_prompt_funct example --annot_method llm --llm_api dummy --output_formatter example --output_file data/raw_datasets/DEMO.txt
```

### Selfplay

Selfplay, alice/bob as single-level llm models
```
python3 do_selfplay.py --alice_type llm_no_planning --bob_type llm_no_planning --llm_api dummy --utt2act_prompt_func example --act2utt_prompt_func example --llm_response_prompt_func example_dia_resp --llm_choice_prompt_func example_choice --context_file data/raw_datasets/dummies/ctx_example.txt --ref_text data/raw_datasets/dummies/ref_example.txt --log_file ../logs/sl_sp_dummy.log
```

Selfplay, alice/bob as dual-level llm models
```
python3 do_selfplay.py --alice_type llm_self_planning --bob_type llm_self_planning --llm_api dummy --utt2act_prompt_func example --act2utt_prompt_func example --llm_response_prompt_func example_dia_resp --llm_choice_prompt_func example_choice --context_file data/raw_datasets/dummies/ctx_example.txt --ref_text data/raw_datasets/dummies/ref_example.txt --log_file ../logs/dl_sp_dummy.log
```

Selfplay, alice/bob as dual-level llm models
```
TODO TODO TODO - python3 do_selfplay.py --alice_type llm_rl_planning --bob_type llm_rl_planning
```

### Chat

Chat with AI as single-level llm agent
```
python3 do_chat.py --ai_type llm_no_planning --llm_api dummy --utt2act_prompt_func example --act2utt_prompt_func example --llm_response_prompt_func example_dia_resp --llm_choice_prompt_func example_choice --context_file data/raw_datasets/dummies/ctx_example.txt --ref_text data/raw_datasets/dummies/ref_example.txt --log_file ../logs/sl_chat_dummy.log
```

Chat with AI as dual-level llm model
```
python3 do_chat.py --ai_type llm_self_planning --llm_api dummy --utt2act_prompt_func example --act2utt_prompt_func example --llm_response_prompt_func example_dia_resp --llm_choice_prompt_func example_choice --context_file data/raw_datasets/dummies/ctx_example.txt --ref_text data/raw_datasets/dummies/ref_example.txt --log_file ../logs/dl_sp_dummy.log
```
