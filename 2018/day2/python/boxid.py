"""
--- Part Two ---
Confident that your list of box IDs is complete, you're ready to find the boxes
full of prototype fabric.

The boxes will have IDs which differ by exactly one character at the same
position in both strings. For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz

The IDs abcde and axcye are close, but they differ by two characters (the
second and fourth). However, the IDs fghij and fguij differ by exactly one
character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above,
this is found by removing the differing character from either ID, producing
fgij.)
"""

import numpy as np


def get_counts_for_string(s):
    vals = {}
    for char in s:
        if char not in vals:
            vals[char] = 0
        vals[char] = vals[char] + 1
    return [2 in vals.values(), 3 in vals.values()]


def test_get_counts_for_string():
    assert get_counts('aarf') == (True, False)
    assert get_counts('abbb3') == (False, True)
    assert get_counts('a84a838') == (True, True)


def get_counts_for_lines(lines):
    return np.sum(np.array([get_counts_for_string(s) for s in lines]), axis=0)


def test_get_counts_for_lines():
    lines = [
        'aarf',
        'abbb3',
        'a94aaa4',
        ]
    counts = get_counts_for_lines(lines)
    assert np.all(counts == np.array([2, 1]))


def number_of_different_characters(s_1, s_2):
    if not len(s_1) == len(s_2):
        raise ValueError("String {} and {} must have same length".format(
            s_1, s_2))
    vals_1 = np.array([ord(x) for x in s_1])
    vals_2 = np.array([ord(x) for x in s_2])
    return len(s_1) - np.sum(vals_1 == vals_2)


def get_data_as_lines(filename):
    with open(filename) as f:
        data = f.read().split('\n')
    if data[-1] == '':
        data.pop(-1)
    return data


## Functions to produce puzzle results from data files

def part_1(filename):
    lines = get_data_as_lines(filename)
    counts = get_counts_for_lines(lines)
    return np.prod(counts)


def part_2(filename):
    lines = get_data_as_lines(filename)
    matching_lines = None
    for i, line_a in enumerate(lines):
        for j, line_b in enumerate(lines):
            # Don't compare a line to itself
            if i == j:
                continue
            diff_chars = number_of_different_characters(line_a, line_b)
            if diff_chars == 1:
                matching_lines = (i, j)
                break
    if matching_lines is None:
        raise RuntimeError("No matching strings found")
    return lines[matching_lines[0]], lines[matching_lines[1]]
