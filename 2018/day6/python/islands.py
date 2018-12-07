"""
In this module, we refer to the points marked in the data file as "centers".
If a given point in the grid is closer to one center than it is to all the other
centers, then that center is the point's "owner".
"""
from collections import namedtuple
import itertools


import numpy as np


SLICE_ALL = slice(None, None, None)


class Point(namedtuple('Point', ['x', 'y'])):

    # Methods to produce neighbors. Note that the coordinate system uses
    # the "graphics" convention (also matrix convention):
    #
    #  012345
    # 0......
    # 1......
    # 2......
    # 3......
    # 4......
    # 5......

    def up(self):
        return Point(self.x, self.y - 1)

    def down(self):
        return Point(self.x, self.y + 1)

    def left(self):
        return Point(self.x - 1, self.y)

    def right(self):
        return Point(self.x + 1, self.y)


def line_to_point(line):
    """Convert a text line to a Point."""
    return Point(*(int(q) for q in line.split(',')))


def load_file_as_tagged_centers(filename):
    """Load a data file as a map from center id to center Point."""
    with open(filename) as f:
        lines = f.read().split('\n')[:-1]  # Drop trailing newline
    centers = [line_to_point(line) for line in lines]
    return {i: center for i, center in enumerate(centers)}


def load_file_as_array(filename):
    """Load a data file as a numeric array.

    Each row corresponds to one center. The first column contains the x
    coordinates, and the second column contains the y coordinates.
    """
    centers = load_file_as_tagged_centers(filename)
    return np.array(
        [[centers[idx].x, centers[idx].y] for idx in range(len(centers))])


def get_distances_and_nearest_centers(centers, point):
    """Get the distances to each center for a point.

    Args:
        centers (np.ndarray): Centers in array form, as returned by
            load_file_as_array.
        point (Point): The point for which we're computing distances to the
            centers.

    Returns:
        np.ndarray: x and y distances to each center
        np.ndarray: Distances to each center
        np.ndarray: id's of centers that are at minimum distance to point
    """
    diffs = np.array([point.x, point.y]) - centers
    distances = np.abs(diffs[:, 0]) + np.abs(diffs[:, 1])
    nearest_centers = np.where(distances==np.min(distances))[0]
    return diffs, distances, nearest_centers


def check_point(centers, claimed_points, point):
    """Find the owner of a point, and decide what adjacent points to check.

    Args:
        centers (np.ndarray): The ith row gives the x/y coordinates of the
            ith center.
        claimed_points (Dict[Point, int]): Maps known points to their owner's
            tag. An owner of None means the point is equally distant to two
            centers.
        point (Point): Where to start searching.

    Returns:
        Optional[int]: Identification of the center that owners point. Also
            called point's "owner". If None, no center owns the point.
        set[Point]: Points adjacent to point that need to be checked.
        bool: If True, point is in an infinite island.
    """
    if point in claimed_points:
        return claimed_points[point], set(), None

    diffs, _, nearest_centers = get_distances_and_nearest_centers(
        centers, point)

    if len(nearest_centers) > 1:
        owner = None
    elif len(nearest_centers) == 1:
        owner = nearest_centers[0]
    else:
        raise RuntimeError("Unreachable")

    additional_points_to_check = set()

    infinite = False
    # Check up?
    if not all(diffs[:, 1] < 0):
        additional_points_to_check.add(point.up())
    else:
        infinite = owner is not None
    # Check down
    if not all(diffs[:, 1] > 0):
        additional_points_to_check.add(point.down())
    else:
        infinite = owner is not None
    # Check right
    if not all(diffs[:, 0] > 0):
        additional_points_to_check.add(point.right())
    else:
        infinite = owner is not None
    # Check left
    if not all(diffs[:, 0] < 0):
        additional_points_to_check.add(point.left())
    else:
        infinite = owner is not None

    return owner, additional_points_to_check, infinite


def get_owners_and_infinites(centers, start_point):
    """Get 
    """
    points_to_check = set([start_point])
    owned_points = {}  # Point -> int
    infinites = set()
    while len(points_to_check):
        point = points_to_check.pop()
        owner, additional_points_to_check, infinite = check_point(
            centers,
            owned_points,
            point,)
        for new_point in additional_points_to_check:
            points_to_check.add(new_point)
        owned_points[point] = owner
        if infinite:
            infinites.add(owner)
    return owned_points, infinites


def compute_scores(owned_points):
    scores = {}
    for owner in owned_points.values():
        score = scores.setdefault(owner, 0)
        scores[owner] = score + 1
    sorted_scores = sorted(
        [(owner, score) for owner, score in scores.items()],
        key=lambda x: x[1],)
    return sorted_scores


def part_1(filename, start_point):
    centers = load_file_as_array(filename)
    owned_points, infinites = get_owners_and_infinites(
        centers,
        start_point,)
    scores = compute_scores(owned_points)
    for owner, score in scores[::-1]:
        if owner not in infinites:
            return score
    raise RuntimeError("No non-infinite island found")


def part_2(filename, start_point=None, max_distance=10000):
    centers = load_file_as_array(filename)

    if start_point is None:
        start_point = Point(
            int(np.mean(centers[:, 0])),
            int(np.mean(centers[:, 1])),)

    points_to_check = set([start_point])
    points_in_island = set()
    points_checked = set()

    while len(points_to_check):
        point = points_to_check.pop()
        points_checked.add(point)

        _, distances, _ = get_distances_and_nearest_centers(
            centers,
            point,)

        if sum(distances) < max_distance:
            points_in_island.add(point)
            for new_point in [
                    point.up(),
                    point.down(),
                    point.left(),
                    point.right(),]:
                if new_point not in points_checked:
                    points_to_check.add(new_point)

    return len(points_in_island)
