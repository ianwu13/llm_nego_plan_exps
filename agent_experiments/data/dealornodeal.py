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

        self.name = 'dnd'
    
    def instance_generator(self, split='train'):
        """Yields instances from the dataset one at a time"""
        max_utt = 8000 if split == 'train' else 1000
        utt_count = 0
        
        for inst in self.dataset_reg[split]:
            yield inst

            utt_count += len(inst['dialogue'].split('<eos>'))
            if utt_count > max_utt:
                break
