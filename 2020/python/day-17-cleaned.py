from functools import partial
from itertools import product
from typing import FrozenSet, List, Tuple
from toolz import compose_left  # type: ignore
from tutils import (
    generate_bounded_coords,
    get_min_max_bounds_from_coords,
    lfilter,
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


def addtuple(t1: Tuple[int, ...], t2: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(map(sum, zip(t1, t2)))


def restore_symmetry(
    dimensional_ordinals: Tuple[int, ...], point: Tuple[int, ...]
) -> FrozenSet[Tuple[int, ...]]:
    """
    For each nth dimension indicated, generate a point that's negative in the
    dimension, with the appropriate combinations where there are multiple
    dimensions involved.

    restore_symmetry((2, 3), (0, 0, 1, 1)) == {
        (0, 0, -1, -1), (0, 0, 1, -1), (0, 0, -1, 1)
    }

    """
    if all([point[n] == 0 for n in dimensional_ordinals]):
        return frozenset()

    new_points = set()
    base_mods = product([1, -1], repeat=len(dimensional_ordinals))
    mods = lfilter(lambda m: not all([x >= 0 for x in m]), base_mods)
    for mod in mods:
        temp_point = [*point]
        for i, ordinal in enumerate(dimensional_ordinals):
            if point[ordinal] > 0:
                temp_point[ordinal] = mod[i] * temp_point[ordinal]

        new_points.add(tuple(temp_point))

    return frozenset(new_points)


def cycle(
    points_on: FrozenSet[Tuple],
    symmetrical_dimensions: Tuple[int, ...] = tuple(),
) -> FrozenSet[Tuple]:
    """
    Because the rules only care about neighbors within one unit, if there's
    symmetry in the starting conditions for a given dimension, then the results
    on each side of the start will be identical and don't need to be
    calculated.
    We're lazy and assume that symmetry only occurs on either side of
    zero--this is true in the data we have, which is symmetrical at the start
    for the z and w dimensions.
    This makes it easy to exclude the negative values for those dimensions when
    we generate the boundaries for the set of points to be considered after
    getting the current bounds from get_min_max_bounds_from_coords and
    expanding by one--we then floor all the minimum bounds at zero for the
    symmetrical dimensions.
    After determining whether a point is active, we also add the versions of
    that point that exist on the negative sides for the symmetrical dimensions.
    """
    new_points = set()
    dimensions = len(next(iter(points_on)))
    transforms = adjacent_transforms(dimensions)
    minimums, maximums = get_min_max_bounds_from_coords(points_on)
    minimums = [_ - 1 for _ in minimums]
    maximums = [_ + 1 for _ in maximums]
    # Exclude negative values in the symmetrical dimensions:
    for sd in symmetrical_dimensions:
        minimums[sd] = max([0, minimums[sd]])
    products = generate_bounded_coords(minimums, maximums)
    for ppoint in products:
        neighbor_candidates = {addtuple(ppoint, tform) for tform in transforms}
        neighbors = neighbor_candidates.intersection(points_on)
        active = False
        if len(neighbors) == 3:
            active = True
        elif len(neighbors) == 2 and ppoint in points_on:
            active = True
        if active:
            new_points.add(ppoint)
            # Add the symmetrical points with negative values:
            for p in restore_symmetry(symmetrical_dimensions, ppoint):
                new_points.add(p)

    return frozenset(new_points)


def process_one(points_on: FrozenSet[Tuple]) -> int:
    # We know there's symmetry if all the values for a dimension are the same:
    sd = [i for i, vals in enumerate(zip(*points_on)) if len(set(vals)) == 1]
    cycle_one = partial(cycle, symmetrical_dimensions=tuple(sd))
    return len(compose_left(*([cycle_one] * 6))(points_on))


def three_to_four(points_on: FrozenSet[Tuple]) -> FrozenSet[Tuple]:
    fours = {(*(p), 0) for p in points_on}
    return frozenset(fours)


def process_two(points_on: FrozenSet[Tuple]) -> int:
    points4 = three_to_four(points_on)
    sd = [i for i, vals in enumerate(zip(*points4)) if len(set(vals)) == 1]
    cycle_two = partial(cycle, symmetrical_dimensions=tuple(sd))
    return len(compose_left(*[*([cycle_two] * 6)])(points4))


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
