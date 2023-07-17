"""
A registry to define the supported datasets, models, and tasks.
"""

# UTIL CLASSES

# Data Handlers
DATA_HANDLER_REG = {
    'dnd': ('data', 'DNDHandler'),
    'casino': ('data', 'CasinoHandler')
}

# LLM APIs
LLM_API_REG = {
    "dummy": ("misc.dummies", "DummyModelHandler"),
    "openai_generic": ("lang_models.llm_apis.open_ai", "OpenAI_Api"),
}
# TODO: THESE ARE NOT YET IMPLEMENTED
'''
"llama_7b": ("lang_models.llm_apis.llama", "Llama7BHandler"),
"falcon_7b": ("lang_models.llm_apis.falcon", "Falcon7BHandler"),
"falcon_40b": ("lang_models.llm_apis.falcon", "Falcon40BHandler"),
"gpt_4": ("lang_models.llm_apis.gpt_4", "GPT_4_Api"),
'''

# ANNOTATIONS

# Prompt List to Annotate Dialogue Instance
# dialogue_instance (format dataset dependent) -> list["prompt_for_annot_single_utt"]
INST2ANNOT_PROMPT_FUN_REG = {
    "example": ("data.conversion.inst2p_functions", "example_inst2p_func"),
    "demo_dnd": ("data.conversion.inst2p_functions", "demo_dnd"),
    "demo_casino": ("data.conversion.inst2p_functions", "demo_casino"),
    "davinci_dnd": ("data.conversion.inst2p_functions", "davinci_dnd_annot_prompt_fun"),
    "davinci_casino": ("data.conversion.inst2p_functions", "davinci_casino_annot_prompt_fun"),
    "gpt_3_5_dnd": ("data.conversion.inst2p_functions", "gpt3_5_dnd_annot_prompt_fun"),
    "gpt_3_5_casino": ("data.conversion.inst2p_functions", "gpt3_5_casino_annot_prompt_fun"),
}

# Dialogue Annotations to Formatted Line Output
# list["dialogue_act_annotations_for_utterances"] -> "single_line_string_output_for_dialogue"
INST_ANNOT2STR_PROMPT_FUN_REG = {
    "example": ("data.conversion.annot2str_functions", "example_annot2s_func"),
    "demo_dnd_outform": ("data.conversion.annot2str_functions", "demo_dnd_outform"),
    "demo_casino_outform": ("data.conversion.annot2str_functions", "demo_casino_outform"),
    "base": ("data.conversion.annot2str_functions", "base_out_formatter"),
    "base_first_line": ("data.conversion.annot2str_functions", "base_out_formatter_first_line")  # Removes content after "\n" character in LLM output
}

# SELFPLAY AND CHAT

# Generator Functions (for planning)
# dialogue_state_json -> list["prompt_to_gen_dialogue_utt_from_act"]
ACT2UTT_PROMPT_FUN_REG = {
    "example": ("lang_models.llm_apis.prompting.act2utt_functions", "example_a2u_func")
}

# Parser Functions (for planning)
# dialogue_state_json -> list["prompt_to_parse_dialogue_act"]
UTT2ACT_PROMPT_FUN_REG = {
    "example": ("lang_models.llm_apis.prompting.utt2act_functions", "example_u2a_func")
}

# Response Generation Functions (dialogue or choice responses)
# dialogue_state_json -> list["prompt_to_gen_response"]
RESPONSE_PROMPT_FUN_REG = {
    "example_dia_resp": ("lang_models.llm_apis.prompting.dia_response_funcitons", "example_dia_response_func"),
    "example_dia_act_resp": ("lang_models.llm_apis.prompting.dia_response_funcitons", "example_dia_act_response_func"),
    "example_choice": ("lang_models.llm_apis.prompting.dia_response_funcitons", "example_choice_func"),
    "dia_resp_slagent_openai_chatcomp": ("lang_models.llm_apis.prompting.dia_response_funcitons", "dia_resp_slagent_openai_chatcomp"),
    "choice_slagent_openai_chatcomp": ("lang_models.llm_apis.prompting.dia_response_funcitons", "choice_slagent_openai_chatcomp"),
}
