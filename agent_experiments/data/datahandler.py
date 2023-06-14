"""
Base class for all datasets.
"""


class BaseDatasetHandler:
    """Base handler for every dataset."""

    def __init__(self, name, args=None):
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
    
    def instance_generator(self):
        """Yields instances from the dataset one at a time"""
        raise NotImplementedError