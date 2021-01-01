from itertools import product
from typing import FrozenSet, List, Iterable, Tuple
from toolz import compose_left  # type: ignore
from tutils import (
    lmap,
    splitstriplines,
    adjacent_transforms,
    load_and_process_input,
    run_tests,
)

DAY = "17"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 112
TA2 = 848
ANSWER1 = 384
ANSWER2 = 2012


def lines_to_points(lines: List[str]) -> FrozenSet[Tuple]:
    """
    We know that only the x and y values will be non-zero at the start, and
    this only deals with the intial input, so we just iterate through the
    lines and columns.
    """
    points_on = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                points_on.add((x, y, 0))
    return frozenset(points_on)


def addtuple(t1: Tuple, t2: Tuple) -> Tuple:
    return tuple(lmap(sum, zip(t1, t2)))


def xget_ranges(points_on: FrozenSet[Tuple]) -> Iterable:
    """
    Given a set of coordinates in n dimensions, return the ranges for each
    dimension that give you the max and min in each dimension for possible
    neighbors (where neighbors are one unit away in any dimension.
    """
    dimensions = len(next(iter(points_on)))
    minimums = [0] * dimensions
    maximums = [0] * dimensions
    # I think the imperative way to do this is faster than the functional
    # approaches I can come up with:
    for point in points_on:
        # for i, number in enumerate(astuple(point)):
        for i, number in enumerate(point):
            if number > maximums[i]:
                maximums[i] = number
            if number < minimums[i]:
                minimums[i] = number
    new_minimums = [_ - 1 for _ in minimums]
    new_maximums = [_ + 2 for _ in maximums]  # extra increment to account
    # for range not being inclusive at the high end
    return (range(*_) for _ in zip(new_minimums, new_maximums))


def get_ranges(points_on: FrozenSet[Tuple]) -> Iterable:
    """
    Given a set of coordinates in n dimensions, return the ranges for each
    dimension that give you the max and min in each dimension for possible
    neighbors (where neighbors are one unit away in any dimension.
    This version optimizes for symmetry in the z and w dimensions
    """
    dimensions = len(next(iter(points_on)))
    minimums = [0] * dimensions
    maximums = [0] * dimensions
    # I think the imperative way to do this is faster than the functional
    # approaches I can come up with:
    for point in points_on:
        # for i, number in enumerate(astuple(point)):
        for i, number in enumerate(point):
            if number > maximums[i]:
                maximums[i] = number
            if number < minimums[i]:
                minimums[i] = number
    new_minimums = [_ - 1 for _ in minimums]
    new_maximums = [_ + 2 for _ in maximums]  # extra increment to account
    # for range not being inclusive at the high end
    new_minimums = new_minimums[:2] + lmap(lambda x: 0, new_minimums[2:])
    # new_maximums = new_maximums[:2] + lmap(abs, new_maximums[2:])
    return (range(*_) for _ in zip(new_minimums, new_maximums))


def cycle(points_on: FrozenSet[Tuple]) -> FrozenSet[Tuple]:
    """
    This version optimizes for symmetry in the z and w dimensions
    """
    new_points = set()
    dimensions = len(next(iter(points_on)))
    transforms = adjacent_transforms(dimensions)
    products = product(*get_ranges(points_on))
    for ppoint in products:
        neighbor_candidates = {addtuple(ppoint, tform) for tform in transforms}
        neighbors = neighbor_candidates.intersection(points_on)
        add = False
        if len(neighbors) == 3:
            add = True
        elif len(neighbors) == 2 and ppoint in points_on:
            add = True
        if add:
            new_points.add(ppoint)
            if dimensions == 3:
                if ppoint[2] > 0:
                    new_points.add((ppoint[0], ppoint[1], -ppoint[2]))
            elif dimensions == 4:
                if ppoint[2] > 0 and ppoint[3] > 0:
                    new_points.add(
                        (ppoint[0], ppoint[1], -ppoint[2], -ppoint[3])
                    )
                if ppoint[2] > 0:
                    new_points.add(
                        (ppoint[0], ppoint[1], -ppoint[2], ppoint[3])
                    )
                if ppoint[3] > 0:
                    new_points.add(
                        (ppoint[0], ppoint[1], ppoint[2], -ppoint[3])
                    )

    return frozenset(new_points)


def xcycle(points_on: FrozenSet[Tuple]) -> FrozenSet[Tuple]:
    new_points = set()
    dimensions = len(next(iter(points_on)))
    transforms = adjacent_transforms(dimensions)
    products = product(*xget_ranges(points_on))
    for ppoint in products:
        neighbor_candidates = {addtuple(ppoint, tform) for tform in transforms}
        neighbors = neighbor_candidates.intersection(points_on)
        if len(neighbors) == 3:
            new_points.add(ppoint)
        elif len(neighbors) == 2 and ppoint in points_on:
            new_points.add(ppoint)
    return frozenset(new_points)


def process_one(points_on: FrozenSet[Tuple]) -> int:
    return len(compose_left(*([cycle] * 6))(points_on))


def three_to_four(points_on: FrozenSet[Tuple]) -> FrozenSet[Tuple]:
    fours = {(*(p), 0) for p in points_on}
    return frozenset(fours)


def process_two(points_on: FrozenSet[Tuple]) -> int:
    procs = [three_to_four, *([cycle] * 6)]
    return len(compose_left(*procs)(points_on))


def cli_main() -> None:
    input_funcs = [splitstriplines, lines_to_points]
    data = load_and_process_input(INPUT, input_funcs)
    initial_points = data.copy()
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process_two(initial_points)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
