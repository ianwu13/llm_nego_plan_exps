"""
If there are many failed API calls, this will fill them for you
"""

import argparse
import json

import utils


def main():
    parser = argparse.ArgumentParser(description='script to fill failed call slots in annotated data')
    parser.add_argument('--llm_api', type=str, default=None,
        help='llm api to be used in annotation')
    parser.add_argument('--llm_api_key', type=str, default=None,
        help='Key to be used when calling provided API')
    parser.add_argument('--in_file', type=str, default=None,
        help='File with failed calls to be filled')
    parser.add_argument('--output_file', type=str,
        help='destination for output file')
    parser.add_argument('--failed_calls_file', type=str,
        help='destination file for failed LLM API calls')
    args = parser.parse_args()

    annot_api = utils.get_llm_api(args.llm_api, args.llm_api_key)

    with open(args.output_file, 'w') as f:
        for line in open(args.in_file, 'r').readlines():
            if 'FAILED' in line:
                sp = line.split('FAILED START ')
                for i, cont in enumerate(sp[1:]):
                    sp2 = cont.split(' END FAILED')
                    try:
                        fc = json.loads(sp2[0].replace('"', '\\"').replace("'}", '"}').replace("'role'", '"role"').replace(" 'content': '", ', "content": "').replace('} {', '}, {').replace("'system'", '"system"').replace("'user'", '"user"').replace("\\'", "'").replace(',,', ','))
                    except:
                        print(sp2[0].replace('"', '\\"').replace("'}", '"}').replace("'role'", '"role"').replace(" 'content': '", ', "content": "').replace('} {', '}, {').replace("'system'", '"system"').replace("'user'", '"user"').replace("\\'", "'"))
                        exit()
                    
                    sp2[0] = annot_api.get_model_outputs([fc])[0]

                    fixed_cont = ''.join(sp2)
                    sp[i+1] = fixed_cont
                
                fixed_line = ''.join(sp)
            else:
                fixed_line = line
            
            f.write(fixed_line)

    with open(args.failed_calls_file, 'w') as f:
        for fc in annot_api.failed_calls:
            f.write(json.dumps(fc) + '\n')

    print("Filling all done.")


if __name__ == '__main__':
    main()
