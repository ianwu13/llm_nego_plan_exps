"""
Handlers for the GRU Local Model.
"""


from lang_models.model import BaseModelHandler


class GRUHandler(BaseModelHandler):
    """Handler for Llama models."""

    def __init__(self, name, args=None):
        """Initialize the model handler."""
        self.name = name
        self.args = args

        # set up the model
        self.setup_model()

    def setup_model(self):
        """Setup the model based on the specific desirable variant. 
        
        Since multiple Llama variants come from the same class, we can probably use the same setup_model() function for all of them.

        The desired variant can be extracted from the args object.
        """
        
        self.model = None

    def get_model_outputs(self, inputs):
        """Get the model outputs.
        
        Args:
            inputs: list of prompts to be passed to the model.

        TODO - we can also shift this method to the parent class if possible.
        """

        outputs = {}
        for item in inputs:
            gen_out = f"This is a dummy output response from the Llama7B model. The first five words of the input are: {' '.join(item.split()[:5])}."
            outputs[item] = gen_out
        
        return outputs
