"""
A registry to define the supported datasets, models, and tasks.
"""


# a set of tuples of the form (dataset_name, model_name, task_name). This formatting might need changes later on.
SUPPORTED_CONFIGS = set([
    ("dnd", "open_ai", "total_item_count"),
])


# a mapping from names to class paths - will help to dynamically load the modules (only what is required) and easily add new ones.
CLS_NAME2PATHS = {
    "nego_datasets": {
        "dnd": "nego_datasets.dealornodeal.DNDHandler",
        "casino": "nego_datasets.casino.CasinoHandler",
    },

    "models": {
        "open_ai": "models.open_ai.OpenAIHandler",
        "llama_7b": "models.llama.Llama7BHandler",
        "falcon_7b": "models.falcon.Falcon7BHandler",
    },

    "tasks": {
        "total_item_count": "tasks.total_item_count.TICHandler",
    }
}