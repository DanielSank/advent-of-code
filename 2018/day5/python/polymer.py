LOWERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
UPPERS = [x.upper() for x in LOWERS]
PAIRS = set((a, b) for a, b in zip(LOWERS, UPPERS))


def test_for_annihilation(a, b):
    """Return Truee if the characters annihilate."""
    if (a, b) in PAIRS or (b, a) in PAIRS:
        return True
    return False


def reduce_polymer(s):
    if len(s) <= 1:
        return s
    result = []
    buf = s[0]
    idx = 1
    while idx < len(s):
        if test_for_annihilation(buf, s[idx]):
            if len(result):
                buf = result.pop(-1)
                idx = idx + 1
            else:
                if len(s[idx:]) >= 3:
                    buf = s[idx + 1]
                    idx = idx + 2
                elif len(s[idx:]) == 2:
                    buf = s[idx + 1]
                    break
                else:
                    return ''.join(result)
        else:
            result.append(buf)
            buf = s[idx]
            idx = idx + 1
    result.append(buf)
    return ''.join(result)


def read_file_to_polymer(filename):
    with open(filename) as f:
        polymer = f.read()
    if polymer[-1] == '\n':
        print("Removing trailing newline")
        polymer = polymer[:-1]
    return polymer


def part_1(filename):
    polymer = read_file_to_polymer(filename)
    return len(reduce_polymer(polymer))


def part_2(filename):
    lengths = set()
    polymer = read_file_to_polymer(filename)
    for pair in PAIRS:
        reduced = ''.join([x if x not in pair else '' for x in polymer])
        lengths.add(len(reduce_polymer(reduced)))
    return min(lengths)
