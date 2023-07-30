#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=18
#SBATCH --time=48:00:00
#SBATCH --account=glucas_540

cd ../..

# setup
module purge
module load conda
eval "$(conda shell.bash hook)"
conda activate llm_exps

# Run script
python3 annotate.py --dataset casino --start_index 24 --annot_method llm --llm_api gpt-3.5-turbo-0613 --llm_api_key FILL_LOCALLY --inst_to_prompt_funct final_casino_cust_form_example --output_formatter base_casino --output_file storage/annot_tests/R2_EVAL_casino_custform_example_gpt35.txt --failed_calls_file data/raw_datasets/FC_casino_custform_example_gpt35.txt
