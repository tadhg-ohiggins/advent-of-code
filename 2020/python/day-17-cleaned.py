import pdb
from functools import partial
from itertools import product
from typing import Callable, FrozenSet, List, Tuple
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
    """
    if len(t1) == 3:
        return (t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2])
    return (
        t1[0] + t2[0],
        t1[1] + t2[1],
        max([0, t1[2] + t2[2]]),
        max([0, t1[3] + t2[3]]),
    )
    """
    # return tuple(a + b for a, b in zip(t1, t2))
    """
    """
    newlist = []
    for a, b in zip(t1, t2):
        newlist.append(a + b)
    return tuple(newlist)
    """
    return tuple(map(sum, zip(t1, t2)))
    """


def restore_symmetry(
    dimensional_ordinals: Tuple[int, ...], point: Tuple[int, ...]
) -> FrozenSet[Tuple[int, ...]]:
    """
    For each nth dimension indicated, generate a point that's negative in the
    dimension, with the appropriate combinations where there are multiple
    dimensions involved.

    restore_symmetry((2, 3), (1, 1, 1, 1)) == {
        (1, 1, -1, -1), (1, 1, 1, -1), (1, 1, -1, 1)
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


def filtered_cycle(
    func: Callable,
    points_on: FrozenSet[Tuple],
) -> FrozenSet[Tuple]:
    """
    func filters the points that should be considered for the evaluation.
    """
    new_points = set()
    dimensions = len(next(iter(points_on)))
    transforms = adjacent_transforms(dimensions)
    point_cache = {}
    for ppoint in points_on:
        if not func(ppoint):
            continue
        neighbor_candidates = {addtuple(ppoint, tform) for tform in transforms}
        for npoint in neighbor_candidates:
            point_cache[npoint] = 1 + point_cache.get(npoint, 0)

    for ppoint in points_on:
        if point_cache.get(ppoint) in (2, 3):
            new_points.add(ppoint)

    for npoint in point_cache:
        if point_cache[npoint] == 3:
            new_points.add(npoint)
    return points_on


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
    z0 = filtered_cycle(lambda x: x[2] == 0, points_on)
    subset = {x for x in points_on if x[2] >= 0}
    # symmetrical_dimensions = tuple()
    """
    points_on = frozenset(
        {
            p
            for p in points_on
            if all([p[n] >= 0 for n in symmetrical_dimensions])
        }
    )
    """

    dimensions = len(next(iter(points_on)))
    transforms = adjacent_transforms(dimensions)
    """
    minimums, maximums = get_min_max_bounds_from_coords(points_on)
    minimums = [_ - 1 for _ in minimums]
    maximums = [_ + 1 for _ in maximums]
    # Exclude negative values in the symmetrical dimensions:
    for sd in symmetrical_dimensions:
        minimums[sd] = max([0, minimums[sd]])
    """
    point_cache = {}
    for ppoint in subset:
        neighbor_candidates = {addtuple(ppoint, tform) for tform in transforms}
        for npoint in neighbor_candidates:
            point_cache[npoint] = 1 + point_cache.get(npoint, 0)

    for ppoint in points_on:
        if point_cache.get(ppoint) in (2, 3):
            if ppoint[2] != 0:
                new_points.add(ppoint)
            if ppoint[2] > 0:
                newpoint = list(ppoint)
                newpoint[2] = -1 * newpoint[2]
                new_points.add(tuple(newpoint))

    for npoint in point_cache:
        if point_cache[npoint] == 3:
            if ppoint[2] != 0:
                new_points.add(ppoint)
            if ppoint[2] > 0:
                newpoint = list(ppoint)
                newpoint[2] = -1 * newpoint[2]
                new_points.add(tuple(newpoint))

    return frozenset(new_points.union(z0))


def process_one(points_on: FrozenSet[Tuple]) -> int:
    # We know there's symmetry if all the values for a dimension are the same:
    sd = [i for i, vals in enumerate(zip(*points_on)) if len(set(vals)) == 1]
    cycle_one = partial(cycle, symmetrical_dimensions=tuple(sd))
    # return len(compose_left(*([cycle_one] * 6))(points_on))
    result = compose_left(*([cycle_one] * 2))(points_on)
    print(result)
    return len(result)
    """
    extra_points = set()
    rs = partial(restore_symmetry, tuple(sd))
    for point in result:
        for p in rs(point):
            extra_points.add(p)
    return len(result.union(extra_points))
    """


def three_to_four(points_on: FrozenSet[Tuple]) -> FrozenSet[Tuple]:
    fours = {(*(p), 0) for p in points_on}
    return frozenset(fours)


def process_two(points_on: FrozenSet[Tuple]) -> int:
    points4 = three_to_four(points_on)
    sd = [i for i, vals in enumerate(zip(*points4)) if len(set(vals)) == 1]
    cycle_two = partial(cycle, symmetrical_dimensions=tuple(sd))
    # return len(compose_left(*[*([cycle_two] * 6)])(points4))
    result = compose_left(*([cycle_two] * 6))(points4)
    print(len(result))
    extra_points = set()
    rs = partial(restore_symmetry, tuple(sd))
    for point in result:
        for p in rs(point):
            extra_points.add(p)
    return len(result.union(extra_points))


def cli_main() -> None:
    input_funcs = [splitstriplines, lines_to_points]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    initial_points = data.copy()
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process_two(initial_points)
    print("Answer two:", answer_two)
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
