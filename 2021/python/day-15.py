from collections import Counter
from functools import cache, partial, reduce
from math import prod
from operator import attrgetter
import pdb
import aoc
import networkx as nx
from toolz import keyfilter, sliding_window

from aoc import Point, adjacent_transforms, generate_bounded_coords
from tadhg_utils import (
    lcompact,
    lconcat,
    lfilter,
    lmap,
    splitstrip,
    splitstriplines,
)


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 40
TA2 = None
A1 = None
A2 = None


def parse_data(data):
    rows = splitstriplines(data)
    grid = {}
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            grid[Point(x=x, y=y)] = int(char)

    return grid


def non_diag_neighbors(point, grid):
    neighbors = []
    if (d := point - Point(x=0, y=1)) in grid:
        neighbors.append(d)
    if (u := point - Point(x=0, y=-1)) in grid:
        neighbors.append(u)
    if (l := point - Point(x=-1, y=0)) in grid:
        neighbors.append(l)
    if (r := point - Point(x=1, y=0)) in grid:
        neighbors.append(r)
    return neighbors


def process_one(grid):
    getx, gety = attrgetter("x"), attrgetter("y")
    xmax, ymax = max(map(getx, grid)), max(map(gety, grid))
    xmin, ymin = min(map(getx, grid)), min(map(gety, grid))
    start, end = Point(xmin, ymin), Point(xmax, ymax)

    graph = nx.Graph()
    # graph.add_nodes_from(grid.keys())
    for point in grid:
        neighbors = non_diag_neighbors(point, grid)
        for pn in neighbors:
            print(point, pn)
            graph.add_edge(point, pn)

    # paths = list(nx.all_simple_paths(graph, start, end))
    paths = find_all_paths(graph, start, end, grid)
    scores = [get_score(grid, p) for p in paths]
    minscore = min(scores) - grid[Point(xmin, ymin)]
    return minscore


def get_score(grid, path):
    return sum([grid[p] for p in path])


def find_all_paths(graph, start, end, grid):
    path = []
    paths = []
    low_score = 20000
    length_limit = 20000
    queue = [(start, end, path)]
    i = 0
    while queue:
        i = i + 1
        # print(i)
        start, end, path = queue.pop()
        path = path + [start]
        score = get_score(grid, path)
        if score > low_score:
            continue
        if len(path) > length_limit:
            # print("too long:", len(path))
            continue
        elif start == end:
            paths.append(path)
            if score < low_score:
                print("new low: ", score)
                print("new length limit: ", len(path) * 1)
                length_limit = len(path) * 1
                low_score = score
        else:
            # nbs = sorted(graph.edges(start), key=lambda x: grid.get(x[1]))
            for node in graph.edges(start):
                # for node in nbs:
                if node[1] != start and node[1] not in path:
                    """
                    print(node[1])
                    print(path)
                    print(node in path)
                    print(end)
                    print("-----")
                    """
                    queue.append((node[1], end, path))

    return paths


def process_two(data):
    pdb.set_trace()
    return data


def cli_main() -> None:
    input_funcs = [parse_data]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    print("Result One:")
    print(result_one)
    result_two = process_two(data)
    aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
"""
--- Day 13: Transparent Origami ---

You reach another volcanically active part of the cave. It would be nice if you
could do some kind of thermal imaging so you could tell ahead of time which
caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you
activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.

Apparently, the Elves have never used this feature. To your surprise, you
manage to find the manual; as you go to open it, page 1 falls out. It's a large
sheet of transparent paper! The transparent paper is marked with random dots
and includes instructions on how to fold it up (your puzzle input). For
example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

The first section is a list of dots on the transparent paper. 0,0 represents
the top-left coordinate. The first value, x, increases to the right. The second
value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0,
and the coordinate 0,7 is below 0,0. The coordinates in this example form the
following pattern, where # is a dot on the paper and . is an empty, unmarked
position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Then, there is a list of fold instructions. Each instruction indicates a line
on the transparent paper and wants you to fold the paper up (for horizontal
y=... lines) or left (for vertical x=... lines). In this example, the first
fold instruction is fold along y=7, which designates the line formed by all of
the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Because this is a horizontal line, fold the bottom half up. Some of the dots
might end up overlapping after the fold is complete, but dots will never appear
exactly on a fold line. The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........

Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the
transparent paper is folded; after the fold is complete, those dots appear in
the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot
just below them in the result (at 0,3) remains visible, as it can be seen
through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge
together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....

Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....

The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the
first fold. After the first fold in the example above, 17 dots are visible -
dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on
your transparent paper?

Your puzzle answer was 631.

--- Part Two ---

Finish folding the transparent paper according to the instructions. The manual
says the code is always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?

Your puzzle answer was EFLFJGRF.
"""
