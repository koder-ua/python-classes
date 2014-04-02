import re
import sys

def iter_lines(fd):
    ch = fd.read(1)
    res = ""
    while ch != '':
        if ch == '\n':
            yield res
            res = ""
        else:
            res += ch
        ch = fd.read(1)
    yield res

def strip_spaces(gen):
    for line in gen:
        yield line.strip()

def drop_empty(gen):
    for line in gen:
        if line != "":
            yield line

int_r = re.compile("\\d+$")
float_r = re.compile("[-]\\d+\\.\d+$")

def split_items(gen):
    for line in gen:
        for elem in line.split():
            if int_r.match(elem):
                yield int(elem)
            elif float_r.match(elem):
                yield float(elem)
            else:
                yield elem

def get_ints(gen):
    for i in gen:
        if isinstance(i, (int, long)):
            yield i

# 1 2 3 4 4.5

if __name__ == "__main__":
    with open(sys.argv[0]) as fd:
        gen = iter_lines(fd)
        gen2 = strip_spaces(gen)
        gen3 = drop_empty(gen2)
        gen4 = split_items(gen3)
        gen5 = get_ints(gen4)
        print "sun of ints =", sum(gen5)
