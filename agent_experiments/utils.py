"""
Common independent utility functions for the summer23-nego-dial package.
"""


import importlib
import json
import os
from registry import CLS_NAME2PATHS


def get_dataset_handler(dataset_name, args):
    """Get the dataset handler."""
    
    # assisted by ChatGPT
    class_name = CLS_NAME2PATHS["nego_datasets"][dataset_name]
    module_name, _, class_name = class_name.rpartition('.')
    module = importlib.import_module(module_name)
    class_to_use = getattr(module, class_name)
    dataset_handler = class_to_use(dataset_name, args)

    return dataset_handler


def get_model_handler(model_name, args):
    """Get the model handler."""

    # assisted by ChatGPT
    class_name = CLS_NAME2PATHS["models"][model_name]
    module_name, _, class_name = class_name.rpartition('.')
    module = importlib.import_module(module_name)
    class_to_use = getattr(module, class_name)
    model_handler = class_to_use(model_name, args)

    return model_handler


def get_task_handler(task_name, args):
    """Get the task handler."""

    # assisted by ChatGPT
    class_name = CLS_NAME2PATHS["tasks"][task_name]
    module_name, _, class_name = class_name.rpartition('.')
    module = importlib.import_module(module_name)
    class_to_use = getattr(module, class_name)
    task_handler = class_to_use(task_name, args)

    return task_handler


def get_output_path(storage_dir, dataset_name, model_name, task_name, num_instances):
    """Construct the output path."""

    return os.path.join(storage_dir, "logs", f"{dataset_name}_{model_name}_{task_name}_{num_instances}.json")


def get_connection_info_path(storage_dir):
    """Construct the path to the connection info for the models."""
    
    return os.path.join(storage_dir, "utilities", "connection_info.json")


def save_json_data(data, out_path):
    """Save the data in a json file."""

    with open(out_path, "w") as f:
        json.dump(data, f, indent=4)