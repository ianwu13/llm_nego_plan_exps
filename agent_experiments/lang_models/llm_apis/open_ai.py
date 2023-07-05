"""
OpenAI models - GPT and variants.
"""

import requests
import json

from lang_models.llm_apis.model import BaseModelHandler

# import openai


class OpenAI_Api(BaseModelHandler):
    """Handler for the OpenAI model."""

    def __init__(
        self, 
        model_name, 
        api_key=None, 
        api_url='https://api.openai.com/v1/completions', 
        prompt_formatter=(lambda x: x), 
        max_tokens=256, 
        temperature=0
    ):
        """Initialize the model handler."""

        assert api_key is not None, 'An API Key is required to use the OpenAI API'
        self.model_name = model_name
        self.api_key = api_key
        self.api_url = api_url

        self.prompt_formatter = prompt_formatter

        self.max_tokens = max_tokens
        self.temperature = temperature

        self.is_llm = True

        # set up the model
        self.setup_model()

    def setup_model(self):
        """Setup the model."""
        # openai.api_key = self.api_key
        pass
    
    '''
    def text_completion(prompt):
        model = "text-davinci-003"
        response = openai.Completion.create(
            engine=model, 
            prompt=prompt, 
            max_tokens=50)
        generated_text = response.choices[0].text
        print("Result from text_completion from OPEN_AI")
        print(generated_text)
        print("----"*10)
        return generated_text
    
    def chat_bot(prompt):
        model = "gpt-3.5-turbo"
        system_prompt = "You are a helpful assistant."
        messages = [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": prompt},
        ]
        response = openai.ChatCompletion.create(
            model = model,
            messages = messages,
            max_tokens = 50
            )
        generated_texts = [
            choice.message["content"].strip() for choice in response["choices"]
        ]
        print("Result from chatbox from OPEN_AI")
        print(generated_texts)
        print("----"*10)
        return generated_texts
    '''

    def get_model_outputs(self, inputs):
        """Get the model outputs.

        Args:
            inputs: list of prompts to be passed to the model.
        """

        outputs = []
        # inputs is a list
        for inp in inputs:

            response = requests.post(
                self.api_url,
                headers={
                    "Content-Type": "application/json", 
                    "Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model_name,
                    "prompt": inp,
                    "max_tokens": self.max_tokens,
                    # "messages": [{"role": "user", "content": "Say this is a test!"}],
                    "temperature": 0.7}
                )
            choices = json.loads(response.content)['choices']
            assert len(choices) == 1, f"Assumed number of responses per prompt would be 1. If this error is raised we need to handle this (len choices={len(choices)})"
            gen_out = choices[0]['text']

            outputs.append(gen_out)

        return outputs
