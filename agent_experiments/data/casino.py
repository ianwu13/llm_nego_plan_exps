"""
CaSiNo dataset: https://huggingface.co/datasets/casino
"""
from datasets import load_dataset

from data.datahandler import BaseDatasetHandler

POINTS_MAP = {
    "Low": 3,
    "Medium": 4,
    "High": 5
}

ORDER_MAP = {
    "Food": 0,
    "Water": 0,
    "Firewood": 0
}


class CasinoHandler(BaseDatasetHandler):
    """Handler for the Casino dataset."""
    MAX_NEGO_PTS = 36

    def setup_dataset(self):
        """
        Setup the dataset.
        Load the data from Huggingface. Do not use any randomization like shuffling here to ensure that the same instances are used for all evaluations.
        """
        casino_dataset = load_dataset("casino")
        self.splits = list(casino_dataset.keys())
        self.dataset_reg = {split: casino_dataset[split] for split in self.splits}

    def get_instances(self, split='train', n=0):
        """Get the instances from the dataset."""
        if n < 1:
            return self.dataset_reg[split]
        elif n == 1:
            return [self.dataset_reg[split][0]]
        else:
            return self.dataset_reg[split][:n]
    
    def instance_generator(self, split):
        """Yields instances from the dataset one at a time"""
        for inst in self.dataset_reg[split]:
            yield inst