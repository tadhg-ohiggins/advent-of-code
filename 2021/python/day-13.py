from functools import cache, partial, reduce
from math import prod
import pdb
import aoc
import networkx as nx
from toolz import keyfilter

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
TA1 = 17
TA2 = None
A1 = 631
A2 = [
    "####.####.#....####...##..##..###..####",
    "#....#....#....#.......#.#..#.#..#.#...",
    "###..###..#....###.....#.#....#..#.###.",
    "#....#....#....#.......#.#.##.###..#...",
    "#....#....#....#....#..#.#..#.#.#..#...",
    "####.#....####.#.....##...###.#..#.#...",
]


def parse_instruction(instruction):
    axis, value = instruction.replace("fold along ", "").split("=")
    return {"axis": axis, "value": int(value)}


def parse_data(data):
    raw_coords, raw_instructions = data.split("\n\n")
    coords = lmap(Point.from_string, splitstriplines(raw_coords))
    instructions = lmap(parse_instruction, splitstriplines(raw_instructions))

    return (coords, instructions)


def splity(coords, instruction, lims):
    _, ymax = lims
    splitline = instruction["value"]
    top_half = lfilter(lambda pt: pt.y < splitline, coords)
    bottom_half = lfilter(lambda pt: pt.y > splitline, coords)
    for point in bottom_half:
        new_point = Point(x=point.x, y=ymax - point.y)
        if new_point not in top_half:
            top_half.append(new_point)
    return top_half


def splitx(coords, instruction, lims):
    xmax, _ = lims
    splitline = instruction["value"]
    left_half = lfilter(lambda pt: pt.x < splitline, coords)
    right_half = lfilter(lambda pt: pt.x > splitline, coords)
    for point in right_half:
        new_point = Point(x=xmax - point.x, y=point.y)
        if new_point not in left_half:
            left_half.append(new_point)
    return left_half


def follow_instructions(coords, instruction, lims):
    if instruction["axis"] == "y":
        return splity(coords, instruction, lims)
    if instruction["axis"] == "x":
        return splitx(coords, instruction, lims)
    raise UserWarning("Unknown axis")


def process_one(data):
    coords, instructions = data
    xmax = sorted(coords, key=lambda p: p.x)[-1].x
    ymax = sorted(coords, key=lambda p: p.y)[-1].y
    count = 0
    for instruction in instructions:
        coords = follow_instructions(coords, instruction, (xmax, ymax))
        count = count + 1
        if count == 1:
            return len(coords)
        xmax = sorted(coords, key=lambda p: p.x)[-1].x
        ymax = sorted(coords, key=lambda p: p.y)[-1].y

    return data


def coords_to_lines(coords, lims):
    grid = [
        Point(*_) for _ in generate_bounded_coords([0, 0], [lims[0], lims[1]])
    ]
    lines = []
    for i in range(lims[1] + 1):
        line = ""
        for pt in filter(lambda p: p.y == i, grid):
            m = "#" if pt in coords else "."
            line = line + m
        lines.append(line)
        print(line)

    return lines


def process_two(data):
    coords, instructions = data
    xmax = sorted(coords, key=lambda p: p.x)[-1].x
    ymax = sorted(coords, key=lambda p: p.y)[-1].y
    for instruction in instructions:
        coords = follow_instructions(coords, instruction, (xmax, ymax))
        xmax = sorted(coords, key=lambda p: p.x)[-1].x
        ymax = sorted(coords, key=lambda p: p.y)[-1].y

    return coords_to_lines(coords, (xmax, ymax))


def cli_main() -> None:
    input_funcs = [parse_data]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
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
