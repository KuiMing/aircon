#!/usr/bin/python3
"""
convert record from mode2 into configure file
"""
import click


def mode2_decode(mode2):
    """
    rearrange record from mode2
    """
    with open(mode2, 'r') as f_file:
        pulse = f_file.read()
    f_file.close()

    pulse = pulse.split("\n")
    pulse = pulse[:-1]
    if pulse[0].split(' ')[0] == 'space':
        pulse = pulse[1:]

    if pulse[-1].split(' ')[0] == 'space':
        pulse = pulse[:-1]

    row = " " * 9
    count = 1
    for i in pulse:
        if count % 6 == 1:
            if count > 1:
                row += "\n"
                row += " " * 9
        pulse = i.split(' ')[1]
        row += " " * (8 - len(pulse)) + pulse
        count += 1
    row += "\n\n"
    command = mode2.split('/')[-1].split('.')[0]
    name = " " * 10 + "name {}\n".format(command)
    return name + row


@click.command()
@click.option('-c', '--conf', help='input configure file')
@click.option('-o', '--output', help='output configure file')
@click.option('--mode2', '-m', multiple=True, defalt=None)
@click.option(
    '--flist',
    '-l',
    help="A text file with list of mode2 log file",
    default=None)
def main(mode2, conf, output, flist):
    """
    convert record from mode2 into configure file
    """
    if flist:
        with open(flist, 'r') as f:
            files = f.read()
        f.close()
        files = files.split('\n')
        files = files[:-1]
    elif mode2:
        files = mode2
    else:
        print("need file list or mode2 log")
    with open(conf, 'r') as f_file:
        temp = f_file.read()
    f_file.close()
    temp = temp.split('begin raw_codes')
    temp[0] += 'begin raw_codes\n\n'
    with open(output, 'w') as f_file:
        f_file.write(temp[0])
        for i in files:
            f_file.write(mode2_decode(i))
        f_file.write("      end raw_codes\n\nend remote\n")
    f_file.close()


if __name__ == '__main__':
    main()
