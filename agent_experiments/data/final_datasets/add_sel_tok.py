from fire import Fire


def main(fpath):
    in_file = open(fpath, 'r')
    lines = in_file.readlines()
    in_file.close()
    out_file = open(fpath, 'w')
    for line in lines:
        if '<no_agreement>' in line.split('<output>'):
            out_file.write(line)
            continue

        new_line_sp = line.split()
        dia_end = new_line_sp.index('</dialogue>')
        last_utt_start = dia_end
        for i in reversed(range(0, dia_end)):
            if new_line_sp[i] in ['YOU:', 'THEM:']:
                last_utt_start = i+1
                break

        new_line_sp = new_line_sp[:last_utt_start] + ['<selection>'] + new_line_sp[dia_end:]

        new_line = ' '.join(new_line_sp)

        out_file.write(new_line + '\n')

    out_file.close()


if __name__ == '__main__':
    Fire(main)