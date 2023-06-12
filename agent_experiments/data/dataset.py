"""
Base class for all datasets.
"""


class BaseDatasetHandler:
    """Base handler for every dataset."""

    def __init__(self, name, args):
        """Initialize the dataset handler."""
        self.name = name
        self.args = args

        # set up the dataset
        self.setup_dataset()

    def setup_dataset(self):
        """Setup the dataset."""
        raise NotImplementedError
    
    def get_instances(self):
        """Get the instances from the dataset.
        
        Uses params from self.args such as num_instances: the required number of instances.
        """
        raise NotImplementedError
    
    def prompts_from_instance(self):
        """Get prompts from individual instances given a formatting function
        """
        raise NotImplementedError