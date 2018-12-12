import re

import marbles


RE = re.compile(r'(\d+) players; last marble is worth (\d+) points: high score is (\d+)')


def get_test_data():
    with open('../test_data.txt') as f:
        text = f.read().split('\n')[:-1]
    return [tuple(int(x) for x in RE.match(line).groups()) for line in text]


def test_part_1():
    for players, last_marble, score in get_test_data():
        assert marbles.part_1(players, last_marble) == score
