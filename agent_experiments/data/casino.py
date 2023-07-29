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
    "Water": 1,
    "Firewood": 2
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

        self.name = 'casino'