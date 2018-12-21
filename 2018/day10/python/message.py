import collections
import re

import numpy as np


number_str = '[-+]?\d+'

RE = re.compile(
    r'position=<\s*?({}),\s*?({})> velocity=<\s*?({}), \s*?({})'.format(
        number_str, number_str, number_str, number_str))


def parse_text_line_as_integers(line):
    return tuple(int(x) for x in RE.match(line).groups())


def load_file_as_integers(filename):
    with open(filename) as f:
        text = f.read().split('\n')[0:-1]
    return [parse_text_line_as_integers(line) for line in text]


def load_file_as_array(filename):
    array = np.array(load_file_as_integers(filename), dtype=int)
    return array[:, 0:2], array[:, 2:]


def render_array(min_x, max_x, min_y, max_y, points):
    img = np.zeros((max_y - min_y + 1, max_x - min_x + 1), dtype=int)
    for point in points:
        img[point[1] - min_y, point[0] - min_x] = 1
    for row in img:
        print(''.join([' ' if ch==0 else '#' for ch in row]))
    print()


def go(filename):
    points, velocities = load_file_as_array(filename)
    frame = 0
    while 1:
        new_points = points + (frame * velocities)
        min_x, min_y = np.min(new_points, axis=0)
        max_x, max_y = np.max(new_points, axis=0)
        print("Extent: {}, {}".format(
            max_x - min_x, max_y - min_y))
        advance_frames = int(input("Advance frame by (0 to render): "))
        frame += advance_frames
        if advance_frames == 0:
            render_array(
                min_x,
                max_x,
                min_y,
                max_y,
                new_points,)
        print("Frame: {}".format(frame))
