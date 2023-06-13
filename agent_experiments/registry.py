"""
A registry to define the supported datasets, models, and tasks.
"""

DATA_HANDLER_REG = {
    'dnd': 'data.dealornodeal.DNDHandler',
    'casino': 'data.casino.CasinoHandler'
}

LLM_API_REG = {
    "llama_7b": "llm_apis.llama.Llama7BHandler",
    "falcon_7b": "models.falcon.Falcon7BHandler",
    "falcon_40b": "models.falcon.Falcon40BHandler",
    "gpt_4": "models.gpt_4.GPT_4_Api",
    "openai_generic": "models.open_ai.OpenAI_Api",
}

I2P_REG = {
    "dnd_Utt2Act": "data.conversion.i2p_functions.dnd_utt_to_act"
}
