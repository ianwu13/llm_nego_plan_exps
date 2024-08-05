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
    - *`commd_gen_selfplay.py`*: script for generating commd of running different experiments and stored as .json and .md file
    - *`extract.py`*: Recursively extract dialogue content from every log file into json format in the provided input directory and stored the result to provided output directory
    - *`get_deal.py`*: detect the final deal from conversation in json format
    - *`get_prompts.py`*:
    - *`registry.py`*: A registry for supported (dataset, model, task) triplets and required name to class mappings.
    - *`utils.py`*: Independent utilities used throughout the code.
    - *`Makefile`*: Automaticly running all the experiment commd in commd.json file

    - `storage/` : SUGGESTED - for all storage, gitignored by default
        - `logs/` : log dir for the results and outputs of the tasks.
        - `utilities/` : additional stuff like commands and API keys for connecting to the models. - should never be pushed to the code repository.

## Data Annotation

- Data annotation can be run using the `annotate/py` script. This script utilizes LLMs to annotate data. The LLM and prompt to use are specified as commnad line arguments when calling the script. Pre-implemented LLM classes and prompts with their respective argument values can be found in `registry.py`.

### Adding a Dataset

- Pipelines have been implemented for the CaSiNo and DND datasets. Datasets are implemented as subclasses of the `BaseDatasetHandler` class found in `agent_experiments/data/datahandler.py`. To add a dataset, simply extend this class and its methods for the new datasets, and add the new class to `registry.py`. Examples of this can be seen in `agent_experiments/data/casino.py` and `agent_experiments/data/dealornodeal.py`

### Adding a Data Annotation pipeline

- Annotation pipelines are specified by the command line arguments provided to `annotate.py` Beyond the LLM and dataset, the most important part is the "--inst_to_prompt_funct" argument, which specifies the function that converts a data point into a prompt to feed the LLM. Examples of these funcitons can be found in `agent_experiments/data/conversion/inst2p_functions.py`.

## Selfplay
- Check the required files and experiment agents parameters in commd_gen_selfplay.py and get the experiment command file by "running: python commd_gen_selfplay.py dataset_name api_key" It will generate two files for each dataset, containing the command for running the selfplay experiment. commd_selfplay_dataset.json (file for makefile to read and run) and commd_selfplay_dataset.md (for human to check command)

- Running all experiment of a dataset by "make dataset_name". (e.g. make casino) The experiment result will be stored as log file under the provided output directory in commands.

- Extract conversation content from log file and store as json format by running "python extract.py dataset". Make sure the input and output directory is valid.

- Get the final deal from GPT by providing the conversation contents, running "python get_deal.py dataset api_key" will append the final deal to the input json file. It will also print the basic stats categorizing different deals and stored as seperate file for each agent_agent scenarios.

## Chat

- bot v. bot chat cna be run using the `do_chat.py` script. Arguments to this script are essentially identical to those for `do_selfplay.py`, but can be specified seperately for each of the bots acting in the negotiations.

***

# Acknowledgements

https://arxiv.org/abs/1512.03385

https://github.com/facebookresearch/end-to-end-negotiator

***

## Adding a new dataset, model, or task

1. Update the registry variables.
2. Follow existing templates in the codebase to add a new class for the dataset, model, or task.

## Formatting Guidelines

- Keep this README up-to-date.
- Use classes and inheritence - as required.
- Follow the naming conventions and line spacing properly - 2 lines for the items in global scope, 1 line for the items within a local scope.
- Add comments properly and add citations to external sources
- Add links in the comments if you copy code directly from any external resource.
- Avoid redundant code - use utils.py to put code that can be shared between multiple classes. Use class inheritence to share any common code.
- Use uniformity (very important)
