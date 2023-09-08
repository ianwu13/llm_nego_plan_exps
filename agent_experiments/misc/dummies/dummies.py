"""
Dummy classes and code for testing pipelines
"""

import sys

from lang_models.llm_apis.model import BaseModelHandler


class DummyModelHandler(BaseModelHandler):

    def __init__(self, model_name):
        super(DummyModelHandler, self).__init__(model_name)
        self.is_llm = True
        self.failed_calls = []

    def setup_model(self):
        pass
    
    def get_model_outputs(self, inputs):
        return inputs

        # input is a list
        # return inputs
        annotated_input = []
        for each in inputs:
            # call the api
            # get annotation from api
            each_annot = '[DUMMY ANNOTATION]'
            annotated_input.append(each_annot)
        return annotated_input
