from functools import partial
from itertools import permutations
from string import ascii_lowercase, ascii_uppercase
import re

from more_itertools import chunked
from toolz import (
    compose_left,
    pipe,
    sliding_window,
)

from tutils import trace, splitblocks
from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    lfilter,
    lmap,  # A version of map that returns a list.
    splitstriplines,
    splitstrip,
    star,
)
import pdb

two_test = [
    "",
    "##..##..##..##..##..##..##..##..##..##..",
    "###...###...###...###...###...###...###.",
    "####....####....####....####....####....",
    "#####.....#####.....#####.....#####.....",
    "######......######......######......####",
    "#######.......#######.......#######.....",
]
two_answer = [
    "",
    "####..##..###...##....##.####...##.####.",
    "...#.#..#.#..#.#..#....#.#.......#....#.",
    "..#..#....###..#..#....#.###.....#...#..",
    ".#...#....#..#.####....#.#.......#..#...",
    "#....#..#.#..#.#..#.#..#.#....#..#.#....",
    "####..##..###..#..#..##..#.....##..####.",
]

TEST_ANSWERS = (13140, "\n".join(two_test))
PUZZLE_ANSWERS = (17940, None)


def parse_line(line):
    if line.strip() == "noop":
        return 0
    else:
        return int(line.split(" ")[1].strip())


def preprocess(data):
    procs = [splitstriplines, cmap(parse_line)]
    result = pipe(data, *procs)
    return result


def part_one(lines):
    data = lines[:]
    cycle, x = 0, 1
    cycles = [20, 60, 100, 140, 180, 220]
    values = []
    stack = []

    while True:
        cycle = cycle + 1
        exc = None
        if stack:
            exc = stack.pop(0)
        if data:
            cmd = data.pop(0)
        else:
            cmd = 0
        if cmd != 0:
            stack.append(0)
            stack.append(cmd)
        else:
            stack.append(0)
        if exc:
            # print(cycle, "exc:", exc)
            x = x + exc
        if cycle in cycles:
            values = values + [cycle * x]

        if not data and not stack:
            break
        if cycle > 220:
            break

    return sum(values)


def part_two(lines):
    data = lines[:]
    cycle, x = 0, 1
    cycles = [40, 80, 120, 160, 200, 240]
    sprite = [0, 1, 2]
    row = 0
    lines = [[]]
    values = []
    stack = []

    while True:
        # print("cycle:", cycle, x, row)
        exc = None
        if stack:
            exc = stack.pop(0)
        if exc:
            # print(x, exc)
            # print(cycle, "exc:", exc)
            x = x + exc
            # pdb.set_trace()
            sprite = [pos + exc for pos in sprite]
            # print(sprite)
        if cycle % 40 in sprite:
            lines[row].append("#")
        else:
            lines[row].append(".")
        if data:
            cmd = data.pop(0)
        else:
            cmd = 0
        if cmd != 0:
            stack.append(0)
            stack.append(cmd)
        else:
            stack.append(0)

        cycle = cycle + 1
        if cycle in cycles:
            # print(lines[row])
            row = row + 1
            lines.append([])

        if not data and not stack:
            break
        if cycle == 240:
            break

    return "\n" + "\n".join("".join(line) for line in lines).strip()
