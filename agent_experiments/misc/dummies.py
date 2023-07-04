"""
Dummy classes and code for testing pipelines
"""

import sys

from lang_models.llm_apis.model import BaseModelHandler


class DummyModelHandler(BaseModelHandler):

    def setup_model(self):
        pass
    
    def get_model_outputs(self, inputs):
        # return inputs
        return ['DUMMY']
