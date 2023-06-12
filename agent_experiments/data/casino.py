"""
CaSiNo dataset: https://huggingface.co/datasets/casino
"""


from data.dataset import BaseDatasetHandler


class CasinoHandler(BaseDatasetHandler):
    """Handler for the Casino dataset."""

    def setup_dataset(self):
        """Setup the dataset.
        
        Load the data from Huggingface. Do not use any randomization like shuffling here to ensure that the same instances are used for all evaluations.
        """
        
        self.dataset = None

    def get_instances(self):
        """Get the instances from the dataset."""

        # last 10 instances from the dataset
        instances = self.dataset[-self.args.num_instances:]
        
        return instances