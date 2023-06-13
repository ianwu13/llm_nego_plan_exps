"""
CaSiNo dataset: https://huggingface.co/datasets/casino
"""
from datasets import load_dataset

from data.datahandler import BaseDatasetHandler


class CasinoHandler(BaseDatasetHandler):
    """Handler for the Casino dataset."""

    def setup_dataset(self):
        """
        Setup the dataset.
        Load the data from Huggingface. Do not use any randomization like shuffling here to ensure that the same instances are used for all evaluations.
        """
        casino_dataset = load_dataset("casino")
        self.splits = list(casino_dataset.keys())
        self.dataset_reg = {split: casino_dataset[split] for split in self.splits}

    def get_instances(self):
        """Get the instances from the dataset."""
        if n < 1:
            return self.dataset_reg[split]
        else:
            return self.dataset_reg[split][:n]
    
    def instance_generator(self):
        """Yields instances from the dataset one at a time"""
        for inst in self.dataset_reg[split]:
            yield inst