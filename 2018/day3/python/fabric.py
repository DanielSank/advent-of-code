"""
Strategy is to stick every square of fabric into a hash bag (set) and keep track
of squares we add twice.
"""
import re
RE = re.compile('#([0-9]+) @ ([0-9]+,[0-9]+): ([0-9]+x[0-9]+)')


def parse_line(line):
    result = RE.match(line)
    identifier, corner, size = result.groups()
    result = [
            int(identifier),
            tuple(int(x) for x in corner.split(',')),
            tuple(int(x) for x in size.split('x')),]
    return result


def get_squares_from_corner_and_size(corner, size):
    for x in range(corner[0], corner[0] + size[0]):
        for y in range(corner[1], corner[1] + size[1]):
            yield x, y


def lines_to_claims(lines):
    return [parse_line(line) for line in lines]


def count_squares_for_claims(claims):
    squares = {}
    for identifier, corner, size in claims:
        for square in get_squares_from_corner_and_size(corner, size):
            squares[square] = squares.setdefault(square, 0) + 1
    return squares


def count_squares_for_lines(lines):
    claims = lines_to_claims(lines)
    return count_squares_for_claims(claims)


def part_1(filename):
    with open(filename) as f:
        lines = f.read().split('\n')
    lines = lines[0:-1]  # Drop trailing blank line
    squares = count_squares_for_lines(lines)
    return sum([x>=2 for x in squares.values()])


def part_2(filename):
    with open(filename) as f:
        lines = f.read().split('\n')[0:-1]
    squares = count_squares_for_lines(lines)
    for identifier, corner, size in lines_to_claims(lines):
        if all(
                squares[square] == 1
                for square in get_squares_from_corner_and_size(corner, size)):
            return identifier
