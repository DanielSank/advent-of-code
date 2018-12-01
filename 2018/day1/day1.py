import itertools


def get_lines(filename):
    with open(filename) as f:
        lines = f.read().split("\n")
        return lines


def process_lines(lines):
    vals = set()

    val = 0
    vals.add(0)

    for line in itertools.cycle(lines):
        if line == '':
            continue
        op = line[0]
        incriment = int(line[1:])
        if op == "-":
            val = val - incriment
        elif op == "+":
            val = val + incriment
        else:
            raise Exception("Operator {} unknown".format(op))
        size = len(vals)
        vals.add(val)
        if not len(vals) > size:
            return val


def go(filename):
    lines = get_lines(filename)
    return process_lines(lines)
