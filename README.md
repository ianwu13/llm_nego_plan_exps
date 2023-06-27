# LLM Negotiation Planning Experiments
Contains code (currently just structure) for experiments on incorporating dialogue planning into LLMs, specifically in the domain of resource negotiation.

## Directory Structure - UPDATE

- `agent_experiments/` : base directory for experiments
    - `agents/` : code/classes for different types of agents, level of interaction (utterance/act, planned/not planned) is handled here
        - *`plan_to_utt_agent.py`* : generates utterance responses based on dialogue act level interactions
        - *`planning_agent.py`* : generates dialogue act responses based on dialogue act history
        - *`utterance_agent.py`* : generates utterance responses based on utterance history
    - `data/` : scripts to return data from different formats/datasets in a consistent format
        - `conversion/` : code to convert/annotate existing datasets to alternative formats
        - `datasets/` : raw files contiaining datasets
    - `interactions/` : code to allow for interaction with/between different models
    - `llm_apis/` : scripts to allow for interfacing with diffferent LLM APIs that are hosted elsewhere
    - `misc/` : miscellaneous one-off scripts for any tasks related to the project - as required.
    - `models/` : weights for dialogue planning models
    - *`do_chat.py`*
    - *`do_selfplay.py`*
    - *`registry.py`*: A registry for supported (dataset, model, task) triplets and required name to class mappings.
    - *`utils.py`*: Independent utilities used throughout the code.

- `storage/` : SUGGESTED - for all storage, gitignored by default
    - `logs/` : log dir for the results and outputs of the tasks.
    - `utilities/` : additional stuff like commands and API keys for connecting to the models. - should never be pushed to the code repository.

## Data Annotation - UPDATE

- TODO

## Adding a Dataset - UPDATE

- TODO

## Adding a Data Annotation pipeline - UPDATE

- TODO

## LLM API Usage - UPDATE

### Adding LLM API

- TODO

### Adding Prompt Generation Funcitons - TODO

- "I2ANNOT_PROMPT_FUN_REG"
- "ACT2UTT_PROMPT_FUN_REG"
- "UTT2ACT_PROMPT_FUN_REG"

## Selfplay - UPDATE

- TODO

## Chat - UPDATE

- TODO

***

# NOT IAN'S

## Adding a new dataset, model, or task

1. Update the registry variables.
2. Follow existing templates in the codebase to add a new class for the dataset, model, or task.

## Running a task

```python main.py --storage_dir ../../storage/ --dataset_name dnd --model_name open_ai  --task_name total_item_count```

## Formatting Guidelines

- Keep this README up-to-date.
- Use classes and inheritence - as required.
- Follow the naming conventions and line spacing properly - 2 lines for the items in global scope, 1 line for the items within a local scope.
- Add comments properly and add citations to external sources
- Add links in the comments if you copy code directly from any external resource.
- Avoid redundant code - use utils.py to put code that can be shared between multiple classes. Use class inheritence to share any common code.
- Use uniformity (very important)
