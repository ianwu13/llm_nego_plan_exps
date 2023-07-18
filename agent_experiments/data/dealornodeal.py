"""
Dealornodeal dataset: https://huggingface.co/datasets/deal_or_no_dialog
"""
from datasets import load_dataset

from data.datahandler import BaseDatasetHandler


class DNDHandler(BaseDatasetHandler):
    """Handler for the DND dataset."""
    MAX_NEGO_PTS = 10

    def setup_dataset(self):
        """
        Setup the dataset. 
        Load the data from Huggingface. Do not use any randomization like shuffling here to ensure that the same instances are used for all evaluations.
        """
        dnd_dataset = load_dataset("deal_or_no_dialog")
        self.splits = list(dnd_dataset.keys())
        self.dataset_reg = {split: dnd_dataset[split] for split in self.splits}

    def get_instances(self, split='train', n=0):
        """Get the instances from the dataset."""
        if n < 1:
            return self.dataset_reg[split]
        elif n == 1:
            return [self.dataset_reg[split][0]]
        else:
            return self.dataset_reg[split][:n]
    
    def instance_generator(self, split='train'):
        """Yields instances from the dataset one at a time"""
        for inst in self.dataset_reg[split]:
            yield inst
