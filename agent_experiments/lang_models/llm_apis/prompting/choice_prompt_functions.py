"""
Functions which convert dialogue instances into LLM prompts to extract the final deal for BOTH agents.
"""
from data.conversion.fs_examples import *

from simple_utils import remove_prefix


def get_casino_final_deal(conv_data):
    """
    call_example: 
        itm_cnts = [self.agents[0].ctx[0], self.agents[0].ctx[2], self.agents[0].ctx[4]]
        choice_prompt = self.cpf({
            'itm_cnts': itm_cnts,
            'alice_ctx': self.agents[0].ctx,
            'bob_ctx': self.agents[0].ctx,
            'dialogue': storage["conv"]
        })
    """
    conv_string = '\n'.join([f"{utt['name']}: {utt['sent']}" for utt in conv_data["dialogue"]])
    prompt = [{'role': 'system', 'content': 'You are assisting the user to detect the final deal of dividing 3 units each of firewood, water, and food in a negotiation dialogue. You should get the final deal in this format "Alice: firewood=X water=X food=X Bob: firewood=X water=X food=X" and fill X with corresponding numbers from conversation. If no deal is reached in the end, fill all X with 0s.'}, 
        {'role': 'user', 'content': f'What is the final deal for this conversation?\n\n {conv_string}'}]
    return [prompt]


def get_dnd_final_deal(conv_data):
    """
    call_example: 
        itm_cnts = [self.agents[0].ctx[0], self.agents[0].ctx[2], self.agents[0].ctx[4]]
        choice_prompt = self.cpf({
            'itm_cnts': itm_cnts,
            'alice_ctx': self.agents[0].ctx,
            'bob_ctx': self.agents[0].ctx,
            'dialogue': storage["conv"]
        })
    """
    conv_string = '\n'.join([f"{utt['name']}: {utt['sent']}" for utt in conv_data["dialogue"]])
    prompt = [{'role': 'system', 'content': f'You are assisting the user to detect the final deal of dividing {conv_data["itm_cnts"][0]} units of books, {conv_data["itm_cnts"][1]} units of hats, and {conv_data["itm_cnts"][2]} units of balls in a negotiation dialogue. You should get the final deal in this format "Alice: book=X hat=X ball=X Bob: book=X hat=X ball=X" and fill X with corresponding numbers from conversation. If no deal is reached in the end, fill all X with 0s.'}, 
        {'role': 'user', 'content': f'What is the final deal for this conversation?\n\n {conv_string}'}]
    return [prompt]
