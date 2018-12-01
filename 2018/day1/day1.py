import itertools


def get_lines(filename):
    "Read a file back as a list of lines."
    with open(filename) as f:
        lines = f.read().split("\n")
        return lines


def process_lines(lines):
    """Cumulatively sum the data until we find a repeated value.

    The data are iterated over cyclicly until we find a repeaet.
    """
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


def part_2(filename):
    """Solve part 2 of the puzzle."""
    lines = get_lines(filename)
    return process_lines(lines)
