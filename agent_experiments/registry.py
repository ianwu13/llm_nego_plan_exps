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
'''
    # THESE ARE NOT YET IMPLEMENTED
    "llama_7b": ("lang_models.llm_apis.llama", "Llama7BHandler"),
    "falcon_7b": ("lang_models.llm_apis.falcon", "Falcon7BHandler"),
    "falcon_40b": ("lang_models.llm_apis.falcon", "Falcon40BHandler"),
'''

# ANNOTATIONS

# Prompt List to Annotate Dialogue Instance
# dialogue_instance (format dataset dependent) -> list["prompt_for_annot_single_utt"]
INST2ANNOT_PROMPT_FUN_REG = {
    # region
    # DEVELOPEMENT TESTS
    # "example": ("data.conversion.inst2p_functions", "example_inst2p_func"),
    # "example_dnd": ("data.conversion.inst2p_functions", "example_inst2p_func_dnd"),
    # "demo_dnd": ("data.conversion.inst2p_functions", "demo_dnd"),
    # "demo_casino": ("data.conversion.inst2p_functions", "demo_casino"),
    # "completion_dnd": ("data.conversion.inst2p_functions", "completion_dnd_annot_prompt_fun"),
    # "completion_casino": ("data.conversion.inst2p_functions", "completion_casino_annot_prompt_fun"),
    # "chat_dnd": ("data.conversion.inst2p_functions", "chat_dnd_annot_prompt_fun"),
    # "chat_casino": ("data.conversion.inst2p_functions", "chat_casino_annot_prompt_fun"),
    # # Final Annotation Prompt Functions (All Chat-Only):
    # "final_dnd_fs": ("data.conversion.inst2p_functions", "final_dnd_fs"),
    # "final_dnd_example": ("data.conversion.inst2p_functions", "final_dnd_example"),
    # "final_casino_dnd_form_fs": ("data.conversion.inst2p_functions", "final_casino_dnd_form_fs"),
    # "final_casino_dnd_form_example": ("data.conversion.inst2p_functions", "final_casino_dnd_form_example"),
    # "final_casino_cust_form_fs": ("data.conversion.inst2p_functions", "final_casino_cust_form_fs"),
    # "final_casino_cust_form_example": ("data.conversion.inst2p_functions", "final_casino_cust_form_example"),

    # # No FS Versions
    # "final_dnd_no_fs": ("data.conversion.inst2p_functions", "final_dnd_no_fs"),
    # "final_casino_dnd_form_no_fs": ("data.conversion.inst2p_functions", "final_casino_dnd_form_no_fs"),
    # "final_casino_cust_form_no_fs": ("data.conversion.inst2p_functions", "final_casino_cust_form_no_fs"),

    # # Description and FS
    # "final_dnd_desc_fs": ("data.conversion.inst2p_functions", "final_dnd_desc_fs"),
    # "final_casino_dnd_form_desc_fs": ("data.conversion.inst2p_functions", "final_casino_dnd_form_desc_fs"),
    # "final_casino_cust_form_desc_fs": ("data.conversion.inst2p_functions", "final_casino_cust_form_desc_fs"),
    # endregion

    # FINAL
    "finalized_dnd": ("data.conversion.inst2p_functions", "finalized_dnd"),
    "finalized_casino_cust_format": ("data.conversion.inst2p_functions", "finalized_casino_cust_format"),

    # Reduced tests
    "reduced_casino_cust_format": ("data.conversion.inst2p_functions", "reduced_casino_cust_format"),
    "context_and_reduced_casino_cust_format": ("data.conversion.inst2p_functions", "context_and_reduced_casino_cust_format"),
    "diahist_and_reduced_casino_cust_format": ("data.conversion.inst2p_functions", "diahist_and_reduced_casino_cust_format"),
    "context_plus_diahist_and_reduced_casino_cust_format": ("data.conversion.inst2p_functions", "context_plus_diahist_and_reduced_casino_cust_format"),
}

# Dialogue Annotations to Formatted Line Output
# list["dialogue_act_annotations_for_utterances"] -> "single_line_string_output_for_dialogue"
INST_ANNOT2STR_PROMPT_FUN_REG = {
    "example": ("data.conversion.annot2str_functions", "example_annot2s_func"),
    "demo_dnd_outform": ("data.conversion.annot2str_functions", "demo_dnd_outform"),
    "demo_casino_outform": ("data.conversion.annot2str_functions", "demo_casino_outform"),
    "base_dnd": ("data.conversion.annot2str_functions", "base_out_formatter_dnd"),
    "base_casino": ("data.conversion.annot2str_functions", "base_out_formatter_casino"),
    "base_first_line_dnd": ("data.conversion.annot2str_functions", "base_out_formatter_first_line_dnd"),  # Removes content after "\n" character in LLM output
    "base_first_line_casino": ("data.conversion.annot2str_functions", "base_out_formatter_first_line_casino"),
    "dnd_lstrip_annotation": ("data.conversion.annot2str_functions", "dnd_lstrip_annotation")
}

# SELFPLAY AND CHAT

# Response Generation Functions (dialogue or choice responses)
# dialogue_state_json -> list["prompt_to_gen_response"]
RESPONSE_PROMPT_FUN_REG = {
    # "example_dia_resp": ("lang_models.llm_apis.prompting.dia_response_funcitons", "example_dia_response_func"),
    # "example_dia_act_resp": ("lang_models.llm_apis.prompting.dia_response_funcitons", "example_dia_act_response_func"),
    # "example_choice": ("lang_models.llm_apis.prompting.dia_response_funcitons", "example_choice_func"),
    # "dia_resp_slagent_completion_dnd": ("lang_models.llm_apis.prompting.dia_response_funcitons", "dia_resp_slagent_completion_dnd"),
    # "choice_slagent_completion_dnd": ("lang_models.llm_apis.prompting.dia_response_funcitons", "choice_slagent_completion_dnd"),
    
    # Human-Bot
    # DND: No planning agents (Single-Level)
    "dia_resp_slagent_chatcomp_dnd": ("lang_models.llm_apis.prompting.dia_response_funcitons", "dia_resp_slagent_chatcomp_dnd"),
    # CaSiNo: No planning agents (Single-Level)
    "dia_resp_slagent_chatcomp_casino": ("lang_models.llm_apis.prompting.dia_response_funcitons", "dia_resp_slagent_chatcomp_casino"),
    # # DND Planning: with planning, function actually do act->act
    # "dia_resp_slagent_chatcomp_dnd_planning": ("lang_models.llm_apis.prompting.dia_response_funcitons", "dia_resp_slagent_chatcomp_dnd_planning"),
    # # CaSiNo Planning: with planning, function actually do act->act
    # "dia_resp_slagent_chatcomp_casino_planning": ("lang_models.llm_apis.prompting.dia_response_funcitons", "dia_resp_slagent_chatcomp_casino_planning"),
    
    # "choice_slagent_chatcomp_dnd": ("lang_models.llm_apis.prompting.dia_response_funcitons", "choice_slagent_chatcomp_dnd"),
    # "choice_slagent_chatcomp_casino": ("lang_models.llm_apis.prompting.dia_response_funcitons", "choice_slagent_chatcomp_casino"),
    
    "dia_resp_slagent_chatcomp_thirdperson_dnd": ("lang_models.llm_apis.prompting.dia_response_funcitons", "dia_resp_slagent_chatcomp_thirdperson_dnd"),
    "choice_slagent_chatcomp_thirdperson_dnd": ("lang_models.llm_apis.prompting.dia_response_funcitons", "choice_slagent_chatcomp_thirdperson_dnd"),
    
    "dia_resp_slagent_chatcomp_thirdperson_casino": ("lang_models.llm_apis.prompting.dia_response_funcitons", "dia_resp_slagent_chatcomp_thirdperson_casino"),
    "choice_slagent_chatcomp_thirdperson_casino": ("lang_models.llm_apis.prompting.dia_response_funcitons", "choice_slagent_chatcomp_thirdperson_casino"),

   # WORK FOR NO PLANNING BUT NEED A ONE WORK FOR PLANNING

    # New added modified agent for dnd
    # 
    "act_act_chatcomp_dnd": ("lang_models.llm_apis.prompting.dia_response_funcitons","act_next_act_dnd"),
    # "act_act_chatcomp_casino_dnd_form": ("lang_models.llm_apis.prompting.dia_response_funcitons","act_act_chatcomp_casino_dnd_form"),
    "act_act_chatcomp_casino_cust_form": ("lang_models.llm_apis.prompting.dia_response_funcitons","act_act_chatcomp_casino_cust_form")
}

# Generator Functions (for planning)
# dialogue_state_json -> list["prompt_to_gen_dialogue_utt_from_act"]
ACT2UTT_PROMPT_FUN_REG = {
    "dnd_a2u_prompt": ("lang_models.llm_apis.prompting.act2utt_functions", "dnd_a2u_prompt"),
    "casino_a2u_prompt": ("lang_models.llm_apis.prompting.act2utt_functions", "casino_a2u_prompt"),
}

# Parser Functions (for planning)
# dialogue_state_json -> list["prompt_to_parse_dialogue_act"]
UTT2ACT_PROMPT_FUN_REG = {
    # "dnd_fs": ("lang_models.llm_apis.prompting.utt2act_functions", "dnd_fs"),
    # "casino_cust_form_fs": ("lang_models.llm_apis.prompting.utt2act_functions", "casino_cust_form_fs"),
    # "casino_dnd_form_fs": ("lang_models.llm_apis.prompting.utt2act_functions", "casino_dnd_form_fs"), # archive version based on final annotation prompt provided by Ian
    
    # Finalized versions (FROM ANNOTATION PIPELINE)
    # "example": ("lang_models.llm_apis.prompting.utt2act_functions", "example_u2a_func"),
    "final_utt2act_dnd": ("lang_models.llm_apis.prompting.utt2act_functions", "final_utt2act_dnd"),
    # "final_utt2act_casino_cust": ("lang_models.llm_apis.prompting.utt2act_functions", "final_utt2act_casino_cust"),

    # CURRENT
    "reduced_casino_cust_format": ("lang_models.llm_apis.prompting.utt2act_functions", "reduced_casino_cust_format"),
}
