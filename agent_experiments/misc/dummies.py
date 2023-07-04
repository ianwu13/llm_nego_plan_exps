"""
Dummy classes and code for testing pipelines
"""

import sys

from lang_models.llm_apis.model import BaseModelHandler


class DummyModelHandler(BaseModelHandler):

    def __init__(self, model_name):
        super(DummyModelHandler, self).__init__(model_name)
        self.is_llm = True

    def setup_model(self):
        pass
    
    def get_model_outputs(self, inputs):
        # return inputs
        return ['DUMMY']
