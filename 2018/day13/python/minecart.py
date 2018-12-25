import collections
import itertools
import os

import numpy as np


CART_ORIENTATIONS = ['<', '^', '>', 'v']

DIFFS = {
        '<': np.array([0, -1]),
        '>': np.array([0, 1]),
        '^': np.array([-1, 0]),
        'v': np.array([1, 0]),
        }
# Displacement for each cart orientation

LEFT = 'left'
STRAIGHT = 'straight'
RIGHT = 'right'

CORNER_TURNS = {
        '/': {
            '>': '^',
            'v': '<',
            '<': 'v',
            '^': '>',
            },
        '\\': {
            '>': 'v',
            'v': '>',
            '<': '^',
            '^': '<',
            },
        }
# Directions the cart should turn to when hitting a corner


def clear_screen():
    os.system('clear')


class Cart:
    """A single cart."""
    def __init__(self, orientation: str, location: np.ndarray):
        self.orientation = orientation
        self.location = location
        self.turns = itertools.cycle([LEFT, STRAIGHT, RIGHT])

    def turn(self):
        """Change the cart orientation when it hits a crossroad '+'."""
        turn = next(self.turns)
        index = CART_ORIENTATIONS.index(self.orientation)
        if turn == STRAIGHT:
            pass
        elif turn == LEFT:
            index -= 1
        elif turn == RIGHT:
            index += 1
        index = index % 4
        self.orientation = CART_ORIENTATIONS[index]

    def get_displacement(self):
        """Get this cart's next displacement"""
        return DIFFS[self.orientation]

    def apply_displacement(self, move: np.ndarray):
        """Apply a displacement to this cart."""
        self.location += move

    # Equality and hashing are done by ID. We do this to maintain cart
    # individuality while allowing them to be stored in a set.

    def __eq__(self, other):
        return id(self) == id(other)

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return "Cart(orientation='{}', location='{}')".format(
            self.orientation, self.location)

    def __str__(self):
        return self.__repr__()


def load_text_from_file(filename):
    with open(filename) as f:
        text = f.read().split('\n')[:-1]
    return np.array(
        [
            [char for char in row]
            for row in text
            ]
        )


def get_initial_carts(grid):
    """Convert text from load_text_from_file to a set of carts and a grid"""
    grid = grid.copy()
    carts = set()
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char in CART_ORIENTATIONS:
                carts.add(Cart(char, np.array([y, x])))
                grid[y, x] = '-' if char in ['<', '>'] else '|'
    return grid, carts


def print_grid(grid, carts):
    clear_screen()
    grid = grid.copy()
    for cart in carts:
        grid[tuple(cart.location)] = cart.orientation
    msg = ''
    for row in grid:
        msg = msg + ''.join(row) + '\n'
    print(msg)
    input()


def displace_carts(grid, carts):
    """Displace a set of carts, and update their orientations."""
    for cart in carts:
        displacement = cart.get_displacement()
        new_location = cart.location + displacement
        char = grid[tuple(new_location)]
        if char == '+':
            cart.turn()
        elif char in ('\\', '/'):
            cart.orientation = CORNER_TURNS[char][cart.orientation]
        elif char in ('-', '|'):
            pass
        cart.apply_displacement(displacement)


def get_collisions(carts):
    """Get all carts that are in the same location as another cart."""
    locations = {}
    for cart in carts:
        locations.setdefault(tuple(cart.location), set()).add(cart)

    collided_carts = set()
    for maybe_collided in locations.values():
        if len(maybe_collided) > 1:
            collided_carts = collided_carts.union(maybe_collided)

    return collided_carts


def part_1(filename, draw=False):
    grid, carts = get_initial_carts(load_text_from_file(filename))
    if draw:
        print_grid(grid, carts)

    while 1:
        collided = set()
        for cart in carts:
            if cart in collided:
                continue
            displace_carts(grid, set([cart]))
            collided.update(get_collisions(carts))
        if draw:
            print_grid(grid, carts)
        if len(collided):
            break

    return tuple(collided.pop().location[::-1])


def part_2(filename, draw=False):
    grid, carts = get_initial_carts(load_text_from_file(filename))
    if draw:
        print_grid(grid, carts)

    while len(carts) > 1:
        collided = set()
        for cart in carts:
            if cart in collided:
                continue
            displace_carts(grid, set([cart]))
            collided.update(get_collisions(carts))
        carts.difference_update(collided)
        if draw:
            print_grid(grid, carts)
    return tuple(carts.pop().location[::-1])
