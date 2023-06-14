"""
A registry to define the supported datasets, models, and tasks.
"""

DATA_HANDLER_REG = {
    'dnd': 'data.dealornodeal.DNDHandler',
    'casino': 'data.casino.CasinoHandler'
}

LLM_API_REG = {
    "openai_generic": "models.open_ai.OpenAI_Api",
    # TODO: THESE ARE NOT YET IMPLEMENTED
    "llama_7b": "llm_apis.llama.Llama7BHandler",
    "falcon_7b": "models.falcon.Falcon7BHandler",
    "falcon_40b": "models.falcon.Falcon40BHandler",
    "gpt_4": "models.gpt_4.GPT_4_Api",
}

I2ANNOT_PROMPT_FUN_REG = {
    "example": "data.conversion.i2p_functions.example_i2p_func",
    "dnd_Utt2Act": "data.conversion.i2p_functions.dnd_utt_to_act"  # TODO: Remove - This does not exist, just example
}

INST_ANNOT2STR_PROMPT_FUN_REG = {
    "example": "data.conversion.annot2str_functions.example_a2s_func"
}

# TODO: IMPLEMENT THESE FUNCTIONS TOO
ACT2UTT_PROMPT_FUN_REG = {}

# TODO: IMPLEMENT THESE FUNCTIONS TOO
UTT2ACT_PROMPT_FUN_REG = {}
