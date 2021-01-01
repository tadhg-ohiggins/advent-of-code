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
"""
--- Day 17: Conway Cubes ---

As your flight slowly drifts through the sky, the Elves at the Mythical
Information Bureau at the North Pole contact you. They'd like some help
debugging a malfunctioning experimental energy source aboard one of their
super-secret imaging satellites.

The experimental energy source is based on cutting-edge technology: a set of
Conway Cubes contained in a pocket dimension! When you hear it's having
problems, you can't help but agree to take a look.

The pocket dimension contains an infinite 3-dimensional grid. At every integer
3-dimensional coordinate (x,y,z), there exists a single cube which is either
active or inactive.

In the initial state of the pocket dimension, almost all cubes start inactive.
The only exception to this is a small flat region of cubes (your puzzle input);
the cubes in this region start in the specified active (#) or inactive (.)
state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes where
any of their coordinates differ by at most 1. For example, given the cube at
x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at
x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to the
following rules:

    If a cube is active and exactly 2 or 3 of its neighbors are also active,
    the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube
    becomes active. Otherwise, the cube remains inactive.

The engineers responsible for this experimental energy source would like you to
simulate the pocket dimension and determine what the configuration of cubes
should be at the end of the six-cycle boot process.

For example, consider the following initial state:

.#.
..#
###

Even though the pocket dimension is 3-dimensional, this initial state
represents a small 2-dimensional slice of it. (In particular, this initial
state defines a 3x3x1 region of the 3-dimensional space.)

Simulating a few cycles from this initial state produces the following
configurations, where the result of each cycle is shown layer-by-layer at each
given z coordinate (and the frame of view follows the active cells in each
cycle):

Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......

After the full six-cycle boot process completes, 112 cubes are left in the
active state.

Starting with your given initial configuration, simulate six cycles. How many
cubes are left in the active state after the sixth cycle?

Your puzzle answer was 384.
--- Part Two ---

For some reason, your simulated results don't match what the experimental
energy source engineers expected. Apparently, the pocket dimension actually has
four spatial dimensions, not three.

The pocket dimension contains an infinite 4-dimensional grid. At every integer
4-dimensional coordinate (x,y,z,w), there exists a single cube (really, a
hypercube) which is still either active or inactive.

Each cube only ever considers its neighbors: any of the 80 other cubes where
any of their coordinates differ by at most 1. For example, given the cube at
x=1,y=2,z=3,w=4, its neighbors include the cube at x=2,y=2,z=3,w=3, the cube at
x=0,y=2,z=3,w=4, and so on.

The initial state of the pocket dimension still consists of a small flat region
of cubes. Furthermore, the same rules for cycle updating still apply: during
each cycle, consider the number of active neighbors of each cube.

For example, consider the same initial state as in the example above. Even
though the pocket dimension is 4-dimensional, this initial state represents a
small 2-dimensional slice of it. (In particular, this initial state defines a
3x3x1x1 region of the 4-dimensional space.)

Simulating a few cycles from this initial state produces the following
configurations, where the result of each cycle is shown layer-by-layer at each
given z and w coordinate:

Before any cycles:

z=0, w=0
.#.
..#
###


After 1 cycle:

z=-1, w=-1
#..
..#
.#.

z=0, w=-1
#..
..#
.#.

z=1, w=-1
#..
..#
.#.

z=-1, w=0
#..
..#
.#.

z=0, w=0
#.#
.##
.#.

z=1, w=0
#..
..#
.#.

z=-1, w=1
#..
..#
.#.

z=0, w=1
#..
..#
.#.

z=1, w=1
#..
..#
.#.


After 2 cycles:

z=-2, w=-2
.....
.....
..#..
.....
.....

z=-1, w=-2
.....
.....
.....
.....
.....

z=0, w=-2
###..
##.##
#...#
.#..#
.###.

z=1, w=-2
.....
.....
.....
.....
.....

z=2, w=-2
.....
.....
..#..
.....
.....

z=-2, w=-1
.....
.....
.....
.....
.....

z=-1, w=-1
.....
.....
.....
.....
.....

z=0, w=-1
.....
.....
.....
.....
.....

z=1, w=-1
.....
.....
.....
.....
.....

z=2, w=-1
.....
.....
.....
.....
.....

z=-2, w=0
###..
##.##
#...#
.#..#
.###.

z=-1, w=0
.....
.....
.....
.....
.....

z=0, w=0
.....
.....
.....
.....
.....

z=1, w=0
.....
.....
.....
.....
.....

z=2, w=0
###..
##.##
#...#
.#..#
.###.

z=-2, w=1
.....
.....
.....
.....

.....

z=-1, w=1
.....
.....
.....
.....
.....

z=0, w=1
.....
.....
.....
.....
.....

z=1, w=1
.....
.....
.....
.....
.....

z=2, w=1
.....
.....
.....
.....
.....

z=-2, w=2
.....
.....
..#..
.....
.....

z=-1, w=2
.....
.....
.....
.....
.....

z=0, w=2
###..
##.##
#...#
.#..#
.###.

z=1, w=2
.....
.....
.....
.....
.....

z=2, w=2
.....
.....
..#..
.....
.....

After the full six-cycle boot process completes, 848 cubes are left in the
active state.

Starting with your given initial configuration, simulate six cycles in a
4-dimensional space. How many cubes are left in the active state after the
sixth cycle?

Your puzzle answer was 2012.
"""
