from functools import partial
from math import prod
from pathlib import Path


def find_totals(target, array):
    for item in array:
        if (target - item) in array:
            # print((target - item) * item)
            return (target - item) * item


def get_values(line):
    rule, pw = line.split(": ")
    rule_range, rule_letter = rule.split(" ")
    rule_min, rule_max = rule_range.split("-")
    return {
        "pw": pw,
        "rule_letter": rule_letter,
        "rule_min": int(rule_min),
        "rule_max": int(rule_max),
    }


def is_valid_pw(item):
    return (
        item["rule_min"]
        <= item["pw"].count(item["rule_letter"])
        <= item["rule_max"]
    )


def is_valid_pw_two(item):
    pw = item["pw"]
    letter = item["rule_letter"]
    mn = item["rule_min"]
    mx = item["rule_max"]
    if pw[mn - 1] == letter and pw[mx - 1] == letter:
        return False
    if pw[mn - 1] == letter or pw[mx - 1] == letter:
        return True
    return False


def count_trees(lines, rightstep, downstep, incr=1):
    lnlen = len(lines[0])
    right = 1
    trees = 0
    for _, ln in enumerate(lines[incr::downstep]):
        right = right + rightstep
        if right > (lnlen - 1):
            right = abs(right - lnlen)
        """
        print(
            ln,
            right,
            ln[: right - 1],
            "|",
            ln[right - 1],
            "|",
            ln[right - 1 :],
        )
        """
        # print(ln[right - 1])
        if ln[right - 1] == "#":
            trees = trees + 1
    print(trees)
    return trees


if __name__ == "__main__":
    raw = list(filter(None, Path("input-03.txt").read_text().splitlines()))
    """
    right = 1
    trees = 0
    for i, line in enumerate(raw[1:]):
        right = right + 3
        if right > 30:
            right = abs(right - 31)
        print(
            line,
            right,
            line[: right - 1],
            "|",
            line[right - 1],
            "|",
            line[right - 1 :],
        )
        # print(line[right - 1])
        if line[right - 1] == "#":
            trees = trees + 1

    print(trees)
    """
    # print(count_trees(raw, 3, 1))
    ct = partial(count_trees, raw)
    vals = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2, 0),
    ]
    print(prod([ct(*v) for v in vals]))

"""
--- Day 3: Toboggan Trajectory ---

With the toboggan login problems resolved, you set off toward the airport.
While travel by toboggan might be easy, it's certainly not safe: there's very
minimal steering and the area is covered in trees. You'll need to see which
angles will take you near the fewest trees.

Due to the local geology, trees in this area only grow on exact integer
coordinates in a grid. You make a map (your puzzle input) of the open squares
(.) and trees (#) you can see. For example:

..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#

These aren't the only trees, though; due to something you read about once
involving arboreal genetics and biome stability, the same pattern repeats to
the right many times:

..##.........##.........##.........##.........##.........##.......  --->
#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........#.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...##....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->

You start on the open square (.) in the top-left corner and need to reach the
bottom (below the bottom-most row on your map).

The toboggan can only follow a few specific slopes (you opted for a cheaper
model that prefers rational numbers); start by counting all the trees you would
encounter for the slope right 3, down 1:

From your starting position at the top-left, check the position that is right 3
and down 1. Then, check the position that is right 3 and down 1 from there, and
so on until you go past the bottom of the map.

The locations you'd check in the above example are marked here with O where
there was an open square and X where there was a tree:

..##.........##.........##.........##.........##.........##.......  --->
#..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........X.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...#X....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->

In this example, traversing the map using this slope would cause you to
encounter 7 trees.

Starting at the top-left corner of your map and following a slope of right 3
and down 1, how many trees would you encounter?

Your puzzle answer was 145.

--- Part Two ---

Time to check the rest of the slopes - you need to minimize the probability of
a sudden arboreal stop, after all.

Determine the number of trees you would encounter if, for each of the following
slopes, you start at the top-left corner and traverse the map all the way to
the bottom:

    Right 1, down 1.
    Right 3, down 1. (This is the slope you already checked.)
    Right 5, down 1.
    Right 7, down 1.
    Right 1, down 2.

In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s)
respectively; multiplied together, these produce the answer 336.

What do you get if you multiply together the number of trees encountered on
each of the listed slopes?

Your puzzle answer was 3424528800.
"""
