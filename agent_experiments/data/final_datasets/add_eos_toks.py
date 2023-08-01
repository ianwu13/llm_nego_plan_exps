from fire import Fire


def main(fpath):
    in_file = open(fpath, 'r')
    lines = in_file.readlines()
    in_file.close()
    out_file = open(fpath, 'w')
    # out_file = open('tmp.txt', 'w')
    for line in lines:
        new_line = line.replace('YOU:', '<eos> YOU:').replace('THEM:', '<eos> THEM:').replace('<dialogue> <eos>', '<dialogue>')
        out_file.write(new_line)

    out_file.close()


if __name__ == '__main__':
    Fire(main)