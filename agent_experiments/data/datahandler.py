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

    def get_instances(self, split='train', n=0):
        """Get the instances from the dataset."""
        if n < 1:
            return self.dataset_reg[split]
        elif n == 1:
            return [self.dataset_reg[split][0]]
        else:
            return self.dataset_reg[split].select(range(n))
    
    def instance_generator(self, split='train'):
        """Yields instances from the dataset one at a time"""
        for inst in self.dataset_reg[split]:
            yield inst