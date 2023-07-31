from fire import Fire


def main(in_file: str='R2_EVAL_casino_custform_example_gpt35_train.txt', out_file: str='casino_cust_fc.txt'):
    retry_prompts = []
    with open(in_file, 'r') as f:
        line = f.readline()
        while line:
            if 'FAILED' in line:
                assert line.count('FAILED START') == 1, 'Code can currently only handle single failed call per line'

                fc_prompt = line.split('FAILED START')[1].split('END FAILED')[0]
                retry_prompts.append(fc_prompt)

            line = f.readline()

    with open(out_file, 'w') as f:
        for fc in retry_prompts:
            f.write(fc + '\n')            


if __name__ == '__main__':
    Fire(main)