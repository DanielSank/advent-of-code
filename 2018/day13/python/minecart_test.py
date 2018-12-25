import numpy as np

import minecart


TEST_GRID = (r'/---\        |   |  /----\| /-+--+-\  || | |  | |  |\-+-/  \-+--/  \------/   ')


def test_cart():
    cart = minecart.Cart('^', (0, 0))
    cart.turn()
    assert cart.orientation == '<'
    cart.turn()
    assert cart.orientation == '<'
    cart.turn()
    assert cart.orientation == '^'
    cart.turn()
    assert cart.orientation == '<'


def test_get_initial_carts():
    grid, carts = minecart.get_initial_carts(
        minecart.load_text_from_file('../test_data_part_1.txt'))

    assert [(cart.orientation, cart.location[0], cart.location[1])
            for cart in sorted(
                list(carts),
                key=lambda c: c.location[0])] == [('>', 0, 2), ('v', 3, 9)]

    for a, b in zip(grid.flatten(), TEST_GRID):
        assert a == b


def test_part_1():
    assert minecart.part_1('../test_data_part_1.txt') == (7, 3)
    assert minecart.part_1('../data.txt') == (43, 111)


def test_part_2():
    assert minecart.part_2('../test_data_part_2.txt') == (6, 4)
    assert minecart.part_2('../test_data_part_2a.txt') == (7, 6)
    assert minecart.part_2('../data.txt') == (44, 56)
