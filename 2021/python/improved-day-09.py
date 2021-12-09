from math import prod
import aoc
from tadhg_utils import lcompact, lfilter, lmap, splitstriplines


INPUT, TEST = aoc.get_inputs(__file__)
TA1, TA2, A1, A2 = 15, 1134, 530, 1019494


def make_grid(data):
    grid = {}
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            grid[aoc.Point(x=x, y=y)] = (char, None)
    return grid


def process_one(data):
    return sum(map(lambda x: x[1][1], get_lows(data)))


def get_lows(grid):
    for pt in grid:
        above = grid.get(aoc.Point(x=pt.x, y=pt.y - 1))
        below = grid.get(aoc.Point(x=pt.x, y=pt.y + 1))
        left = grid.get(aoc.Point(x=pt.x - 1, y=pt.y))
        right = grid.get(aoc.Point(x=pt.x + 1, y=pt.y))
        adjs = lcompact([above, below, left, right])
        curr = int(grid[pt][0])
        low = True
        for adj in adjs:
            if curr >= int(adj[0]):
                low = False
        if low:
            grid[pt] = (grid[pt][0], curr + 1)

    lows = lfilter(lambda x: x[1][1] is not None, grid.items())

    return lows


def explore(grid, start, future, basin, xmax, ymax):
    dirs = []
    if start.x > 0:
        dirs.append(aoc.Point(x=start.x - 1, y=start.y))
    if start.x < xmax:
        dirs.append(aoc.Point(x=start.x + 1, y=start.y))
    if start.y > 0:
        dirs.append(aoc.Point(x=start.x, y=start.y - 1))
    if start.y < ymax:
        dirs.append(aoc.Point(x=start.x, y=start.y + 1))

    near = {k: grid[k] for k in dirs if k not in basin}

    for pt, data in near.items():
        if data and int(data[0]) not in (None, 9):
            if pt not in future:
                future.append(pt)
            if pt not in basin:
                basin.append(pt)

    for pt in future:
        basin = explore(grid, pt, [], basin, xmax, ymax)

    return basin


def process_two(grid):
    lows = get_lows(grid)

    xmax = sorted(grid.keys(), key=lambda p: p.x)[-1].x
    ymax = sorted(grid.keys(), key=lambda p: p.y)[-1].y
    basins = lmap(lambda x: explore(grid, x[0], [], [x[0]], xmax, ymax), lows)
    sbasins = sorted(basins, key=len)
    threebasins = sbasins[-3:]
    return prod(map(len, threebasins))


def cli_main() -> None:
    input_funcs = [splitstriplines, make_grid]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    print(result_one)
    result_two = process_two(data)
    aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
"""
--- Day 9: Smoke Basin ---

These caves seem to be lava tubes. Parts are even still volcanically active;
small hydrothermal vents release smoke into the caves that slowly settles like
rain.

If you can model how the smoke flows through the caves, you might be able to
avoid it and be that much safer. The submarine generates a heightmap of the
floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the
following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the
highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than
any of its adjacent locations. Most locations have four adjacent locations (up,
down, left, and right); locations on the edge or corner of the map have three
or two adjacent locations, respectively. (Diagonal locations do not count as
adjacent.)

In the above example, there are four low points, all highlighted: two are in
the first row (a 1 and a 0), one is in the third row (a 5), and one is in the
bottom row (also a 5). All other locations on the heightmap have some lower
adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the
risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of
all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk
levels of all low points on your heightmap?

Your puzzle answer was 530.
--- Part Two ---

Next, you need to find the largest basins so you know what areas are most
important to avoid.

A basin is all locations that eventually flow downward to a single low point.
Therefore, every low point has a basin, although some basins are very small.
Locations of height 9 do not count as being in any basin, and all other
locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the
low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678

The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678

The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

Find the three largest basins and multiply their sizes together. In the above
example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?

Your puzzle answer was 1019494.
"""
