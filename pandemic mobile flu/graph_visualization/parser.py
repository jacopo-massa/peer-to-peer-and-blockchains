import math
import sys


def roundup(x):
    return math.ceil(x / 1000.0) * 1000


def parse(filename):
    file = open(filename, 'r')
    lines = file.readlines()

    n_peers = int(lines[0].rstrip("\n"))

    infections = []
    patched = {}

    for line in lines[1:]:
        parts = line.rstrip("\n").split(',', 3)
        if len(parts) == 3:  # INFECTED
            node = parts[0]
            other_node = parts[1]
            cycle = roundup(int(parts[2]))

            infections.append((node, other_node, {'cycle': cycle}))

        elif len(parts) == 2:  # PATCH
            node = parts[0]
            cycle = roundup(int(parts[1]))

            patched[node] = cycle

        else:
            print("Not valid line", file=sys.stderr)

    return n_peers, infections, patched


if __name__ == '__main__':
    print(parse('contacts.txt'))
