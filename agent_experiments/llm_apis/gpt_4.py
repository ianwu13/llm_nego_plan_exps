"""
OpenAI models - GPT and variants.
"""


from models.model import BaseModelHandler


class GPT_4_Api(BaseModelHandler):
    """Handler for the OpenAI model."""

    def setup_model(self):
        """Setup the model."""
        
        self.model = None

    def get_model_outputs(self, inputs):
        """Get the model outputs.
        
        Args:
            inputs: list of prompts to be passed to the model.
        """

        outputs = {}
        for item in inputs:
            gen_out = f"This is a dummy output response from the OpenAI model. The first five words of the input are: {' '.join(item.split()[:5])}."
            outputs[item] = gen_out
        
        return outputs