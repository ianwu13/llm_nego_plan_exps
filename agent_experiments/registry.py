"""
A registry to define the supported datasets, models, and tasks.
"""

DATA_HANDLER_REG = {
    'dnd': ('data', 'DNDHandler'),
    'casino': ('data', 'CasinoHandler')
}

LLM_API_REG = {
    "openai_generic": ("lang_models.llm_apis.open_ai", "OpenAI_Api"),
    # TODO: THESE ARE NOT YET IMPLEMENTED
    "llama_7b": ("lang_models.llm_apis.llama", "Llama7BHandler"),
    "falcon_7b": ("lang_models.llm_apis.falcon", "Falcon7BHandler"),
    "falcon_40b": ("lang_models.llm_apis.falcon", "Falcon40BHandler"),
    "gpt_4": ("lang_models.llm_apis.gpt_4", "GPT_4_Api"),
}

INST2ANNOT_PROMPT_FUN_REG = {
    "example": ("data.conversion.inst2p_functions", "example_inst2p_func"),  # TODO: COMMENTS EXPLAINING PATTERN IN HERE
}

INST_ANNOT2STR_PROMPT_FUN_REG = {
    "example": ("data.conversion.annot2str_functions", "example_annot2s_func")  # TODO: COMMENTS EXPLAINING PATTERN IN HERE
}

ACT2UTT_PROMPT_FUN_REG = {
    "example": ("lang_models.llm_apis.prompting.act2utt_functions", "example_a2u_func")  # TODO: COMMENTS EXPLAINING PATTERN IN HERE
}

UTT2ACT_PROMPT_FUN_REG = {
    "example": ("lang_models.llm_apis.prompting.utt2act_functions", "example_u2a_func")  # TODO: COMMENTS EXPLAINING PATTERN IN HERE
}
