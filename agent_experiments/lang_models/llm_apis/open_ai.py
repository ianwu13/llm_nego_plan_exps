"""
OpenAI models - GPT and variants.
"""

import re
import requests
import json
import time

from lang_models.llm_apis.model import BaseModelHandler

# import openai


class OpenAI_Api(BaseModelHandler):
    """Handler for the OpenAI model."""

    def __init__(
        self, 
        model_name, 
        api_key=None, 
        api_url='https://api.openai.com/v1/chat/completions', 
        prompt_formatter=(lambda x: x), 
        max_tokens=256, 
        temperature=0
    ):
        """Initialize the model handler."""

        assert api_key is not None, 'An API Key is required to use the OpenAI API'
        self.model_name = model_name
        self.api_key = api_key

        if self.model_name.startswith('text-'):
            self.api_url = 'https://api.openai.com/v1/completions'
            self.legacy = True
        else:
            self.api_url = api_url
            self.legacy = False

        self.prompt_formatter = prompt_formatter

        self.max_tokens = max_tokens
        self.temperature = temperature

        self.is_llm = True
        self.failed_calls = {}

        # set up the model
        self.setup_model()

    def setup_model(self):
        """Setup the model."""
        # openai.api_key = self.api_key
        pass
    
    def get_legacy_completions_out(self, inputs):
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
                    "temperature": 0}
                )
            choices = json.loads(response.content)['choices']
            assert len(choices) == 1, f"Assumed number of responses per prompt would be 1. If this error is raised we need to handle this (len choices={len(choices)}; {choices})"
            gen_out = choices[0]['text'].strip('\n')

            # Remove non-alphanumeric characters nad make lowercase
            gen_out = re.sub(r'[^A-Za-z0-9<> ]+', '', gen_out).lower()

            outputs.append(gen_out)

        return outputs

    def get_chat_completions_out(self, inputs):
        """
        import openai

        openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"}
            ]
        )
        """
        outputs = []
        # inputs is a list
        for inp in inputs:
            req_headers = {
                    "Content-Type": "application/json", 
                    "Authorization": f"Bearer {self.api_key}"}
            req_json = {
                    "model": self.model_name,
                    "messages": inp,
                    "temperature": 0}
        
            response = requests.post(
                self.api_url,
                headers=req_headers,
                json=req_json
                )

            # Handle API hanging
            if response.status_code != 200:
                # if response.status_code == 503:
                for _ in range(3):  # Do 3 retrys
                    time.sleep(1)  # Let API cool down
                    response = requests.post(
                        self.api_url,
                        headers=req_headers,
                        json=req_json
                        )
                    if response.status_code == 200:
                        break
                
                if response.status_code != 200:
                    failed_call_id = hash(inp)
                    self.failed_calls[failed_call_id] = inp
                    p_str = str(inp).replace('\n', '')
                    # print("OPENAI ISSUE")
                    # print(f'Response Error Code: {response.status_code}')
                    # print()
                    # print(response.content)
                    # print()
                    # raise Exception('OpenAI API Failed Call')
                    outputs.append(' '.join(['<FAILED_CALL>', str(failed_call_id), '</FAILED_CALL>']))
                    continue

            try:
                choices = json.loads(response.content)['choices']
            except:
                print('='*100)
                print(response)
                print('-'*100)
                print(response.content)
                print('-'*100)
                raise Exception("KeyError: 'choices' in API response")
            assert len(choices) == 1, f"Assumed number of responses per prompt would be 1. If this error is raised we need to handle this (len choices={len(choices)}; {choices})"
            # In Python, the assistant’s reply can be extracted with response['choices'][0]['message']['content']
            gen_out = choices[0]['message']['content'].strip('\n').replace('\n', ' ')

            # Remove non-alphanumeric characters nad make lowercase
            gen_out = re.sub(r'[^A-Za-z0-9<>=/, ]+', '', gen_out).lower()

            outputs.append(gen_out)

        return outputs

    def get_model_outputs(self, inputs):
        if self.legacy:
            return self.get_legacy_completions_out(inputs)
        else:
            return self.get_chat_completions_out(inputs)
