from functools import reduce
from itertools import starmap
from operator import attrgetter
import aoc
from toolz import compose_left, groupby

from aoc import Point, generate_bounded_coords
from tadhg_utils import lmap, splitstriplines


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 17
TA2 = None
A1 = 631
A2 = [
    "████ ████ █    ████   ██  ██  ███  ████",
    "█    █    █    █       █ █  █ █  █ █   ",
    "███  ███  █    ███     █ █    █  █ ███ ",
    "█    █    █    █       █ █ ██ ███  █   ",
    "█    █    █    █    █  █ █  █ █ █  █   ",
    "████ █    ████ █     ██   ███ █  █ █   ",
]


def parse_instruction(instruction):
    axis, value = instruction.replace("fold along ", "").split("=")
    return {"axis": axis, "value": int(value)}


def parse_data(data):
    raw_coords, raw_instructions = map(splitstriplines, data.split("\n\n"))
    coords = lmap(Point.from_string, raw_coords)
    instructions = lmap(parse_instruction, raw_instructions)
    return (coords, instructions)


def do_fold(coords, fold):
    axis, line, getaxis = fold["axis"], fold["value"], attrgetter(fold["axis"])
    divide = lambda pt: "-" if getaxis(pt) == line else getaxis(pt) < line
    # Note that we know that the values of these will always be > line:
    mirrorx = lambda pt: Point(x=pt.x - (2 * (pt.x - line)), y=pt.y)
    mirrory = lambda pt: Point(x=pt.x, y=pt.y - (2 * (pt.y - line)))
    transform = mirrorx if axis == "x" else mirrory
    halves = groupby(divide, coords)
    newpoints = map(transform, halves[False])
    return list(set(halves[True]).union(newpoints))


def process_one(data):
    coords, instructions = data
    return len(do_fold(coords, instructions[0]))


def coords_to_lines(coords):
    getx, gety = attrgetter("x"), attrgetter("y")
    xmax, ymax = max(map(getx, coords)), max(map(gety, coords))
    lstarmap = compose_left(starmap, list)
    grid = lstarmap(Point, generate_bounded_coords([0, 0], (xmax, ymax)))

    def get_line(idx):
        display = lambda pt: "█" if pt in coords else " "
        return "".join(map(display, filter(lambda p: p.y == idx, grid)))

    return lmap(get_line, range(ymax + 1))


def process_two(data):
    coords, instructions = data
    coords = reduce(do_fold, instructions, coords)
    result = coords_to_lines(coords)
    print("\n".join(result))
    return result


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
