"""
Dealornodeal dataset: https://huggingface.co/datasets/deal_or_no_dialog
"""


from nego_datasets.dataset import BaseDatasetHandler


class DNDHandler(BaseDatasetHandler):
    """Handler for the DND dataset."""

    def setup_dataset(self):
        """Setup the dataset.
        
        Load the data from Huggingface. Do not use any randomization like shuffling here to ensure that the same instances are used for all evaluations.
        """
        
        self.dataset = [
            {
                "dialogue": "dummy dialogue one",
            },
            {
                "dialogue": "dummy dialogue two",
            },
        ]

    def get_instances(self):
        """Get the instances from the dataset."""

        # last 10 instances from the dataset
        instances = self.dataset[-self.args.num_instances:]
        
        return instances