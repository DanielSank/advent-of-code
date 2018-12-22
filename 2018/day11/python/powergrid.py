import functools
import itertools

import numpy as np


SERIAL = 1308


def compute_power(x: int, y: int, serial: int) -> int:
    """Compute the power of a single cell.

    Args:
        x: the x-coordinate
        y: the y-corrdinate
        serial: the grid's serial number

    Returns:
        The power value of the cell.
    """
    rack_id = x + 10
    val = str(((rack_id * y) + serial) * rack_id)
    if len(val) < 3:
        return 0
    return int(val[-3]) - 5


def make_cells(serial):
    func = functools.partial(compute_power, serial=serial)
    xs = np.linspace(1, 300, 300, dtype=int)
    ys = np.linspace(1, 300, 300, dtype=int)
    cells = np.zeros((300, 300))
    for x, y in itertools.product(xs, ys):
        cells[y-1, x-1] = compute_power(x, y, serial)
    return cells


def compute_patch_powers(cells, kernel_size):
    kernel = np.ones(kernel_size)
    convolved = np.vstack(
        np.convolve(row, kernel, mode='valid') for row in cells)
    convolved = np.vstack(
        np.convolve(col, kernel, mode='valid') for col in convolved.T).T
    index = np.unravel_index(np.argmax(convolved, axis=None), convolved.shape)
    return index, convolved[index]


def part_1(serial=SERIAL):
    cells = make_cells(serial)
    index, _ = compute_patch_powers(cells, kernel_size=3)
    return index[1] + 1, index[0] + 1  # Respect the puzzle's coordinate system


def part_2(serial=SERIAL):
    max_power = 0
    max_index = None
    max_size = None
    cells = make_cells(serial)

    for kernel_size in np.linspace(1, 300, 300, dtype=int):
        index, power = compute_patch_powers(cells, kernel_size)
        if power > max_power:
            max_power = power
            max_index = index
            max_size = kernel_size
    return max_index[1] + 1, max_index[0] + 1, max_size
