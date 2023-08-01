from fire import Fire


def main(fpath):
    in_file = open(fpath, 'r')
    lines = in_file.readlines()
    in_file.close()
    out_file = open(fpath, 'w')
    # out_file = open('tmp.txt', 'w')
    for line in lines:
        new_line_sp = line.split(' <output> ')
        sp2 = new_line_sp[1].split(' </output> ')

        sp3 = sp2[0].split()

        tmp = sp3[0]
        sp3[0] = sp3[2]
        sp3[2] = tmp

        tmp = sp3[3]
        sp3[3] = sp3[5]
        sp3[5] = tmp

        sp2[0] = ' '.join(sp3).replace('Firewood', 'item2').replace('Water', 'item1').replace('Food', 'item0')

        new_line_sp[1] = ' </output> '.join(sp2)

        new_line = ' <output> '.join(new_line_sp)
        out_file.write(new_line)

    out_file.close()


if __name__ == '__main__':
    Fire(main)