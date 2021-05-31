from __future__ import annotations
from tutils import Point
from tutils import partial
from tutils import reduce
from tutils import Any
from tutils import unique
from tutils import mapcat

from tutils import load_and_process_input
from tutils import run_tests


""" END HELPER FUNCTIONS """


DAY = "03"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = None
TA2 = None
ANSWER1 = 2565
ANSWER2 = 2639


def cli_main() -> None:
    input_funcs = [str.strip]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process_two(data)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


def process_one(data: str) -> Any:
    return len(from_origin(data))


def visit(coords: Point, directions: str):
    visitor = lambda arr, pt: arr + [move(arr[-1], pt)]
    visited = reduce(visitor, directions, [coords])

    return list(unique(map(str, visited)))


from_origin = partial(visit, Point(0, 0))


def move(coords: Point, direction: str):
    dirs = {
        "^": Point(1, 0),
        "v": Point(-1, 0),
        ">": Point(0, 1),
        "<": Point(0, -1),
    }
    return coords + dirs[direction]


def process_two(data: str) -> Any:
    santa_robosanta = (data[::2], data[1::2])
    points = unique(mapcat(from_origin, santa_robosanta))
    return len(list(points))


if __name__ == "__main__":
    cli_main()


"""
--- Day 3: Perfectly Spherical Houses in a Vacuum ---

Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and
then an elf at the North Pole calls him via radio and tells him where to move
next. Moves are always exactly one house to the north (^), south (v), east (>),
or west (<). After each move, he delivers another present to the house at his
new location.

However, the elf back at the north pole has had a little too much eggnog, and
so his directions are a little off, and Santa ends up visiting some houses more
than once. How many houses receive at least one present?

For example:

    > delivers presents to 2 houses: one at the starting location, and one to
    the east.
    ^>v< delivers presents to 4 houses in a square, including twice to the
    house at his starting/ending location.
    ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only
    2 houses.

Your puzzle answer was 2565.
--- Part Two ---

The next year, to speed up the process, Santa creates a robot version of
himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the
same starting house), then take turns moving based on instructions from the
elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

    ^v delivers presents to 3 houses, because Santa goes north, and then
    Robo-Santa goes south.
    ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up
    back where they started.
    ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one
    direction and Robo-Santa going the other.

Your puzzle answer was 2639.
"""
