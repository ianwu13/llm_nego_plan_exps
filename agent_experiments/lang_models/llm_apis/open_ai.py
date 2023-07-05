"""
OpenAI models - GPT and variants.
"""

import requests
import json

from lang_models.llm_apis.model import BaseModelHandler

import openai


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
        print("set up model")
        self.model = None

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
            assert len(choices == 1), "Assumed number of responses per prompt would be 1. If this error is raised we need to handle this"
            gen_out = choices[0]['text']

            outputs.append(gen_out)

        return outputs
