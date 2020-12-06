from functools import partial
from pathlib import Path
from typing import Iterable
from toolz import (  # type: ignore
    compose_left,
    concat,
)


IterableS = Iterable[str]


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]


def get_coords(text):
    start, end = text.split(" through ")
    start_coords = lmap(int, start.split(","))
    end_coords = lmap(int, end.split(","))
    return start_coords, end_coords


def alter(val, command):
    if command == "on":
        return 1
    elif command == "off":
        return 0
    elif command == "toggle":
        return int(not bool(val))


def alter2(val, command):
    if command == "on":
        return val + 1
    elif command == "off":
        return max([0, val - 1])
    elif command == "toggle":
        return val + 2


def change(func, grid, text, command):
    start, end = get_coords(text)
    for j in range(start[1], end[1] + 1):
        for i in range(start[0], end[0] + 1):
            grid[j][i] = func(grid[j][i], command)
    return grid


change1 = partial(change, alter)
change2 = partial(change, alter2)


def instr(func, grid, text):
    if text.startswith("turn on "):
        return func(grid, text.removeprefix("turn on "), "on")
    elif text.startswith("turn off "):
        return func(grid, text.removeprefix("turn off "), "off")
    elif text.startswith("toggle"):
        return func(grid, text.removeprefix("toggle"), "toggle")


instr1 = partial(instr, change1)
instr2 = partial(instr, change2)


def process(lights, lines, func):
    lines = lfilter(None, lines)
    for line in lines:
        lights = func(lights[:], line.strip())
    return sum(list(concat(lights)))


if __name__ == "__main__":
    # test = Path("09-test-data.txt").read_text()
    # test_answer = whatever
    # assert process(test, params) == test_answer

    raw = Path("input-06.txt").read_text()
    raw = raw.strip()

    lights = [[0] * 1000 for i in range(0, 1000)]
    test_lights = [[0] * 1000 for i in range(0, 1000)]
    testb_lights = [[0] * 1000 for i in range(0, 1000)]
    one_passing = [
        "turn on 0,0 through 999,999",
        "turn off 0,0 through 999,999",
        "turn on 0,0 through 999,0",
        "toggle 499,499 through 500,500",
    ]
    results = process(test_lights, one_passing, instr1)
    assert results == 1004

    oneb_passing = [
        "turn on 0,0 through 999,999",
        "toggle 499,499 through 500,500",
    ]
    # assert not any([process(_) for _ in one_failing])
    resultsb = process(testb_lights, oneb_passing, instr1)
    assert resultsb == 999996
    answer = process(lights, raw.splitlines(), instr1)
    assert answer == 400410
    two_lights = [[0] * 1000 for i in range(0, 1000)]
    answer2 = process(two_lights, raw.splitlines(), instr2)
    assert answer2 == 15343601
    print(answer, answer2)


"""
--- Day 6: Probably a Fire Hazard ---

Because your neighbors keep defeating you in the holiday house decorating
contest year after year, you've decided to deploy one million lights in a
1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed
you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at
each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include
whether to turn on, turn off, or toggle various inclusive ranges given as
coordinate pairs. Each coordinate pair represents opposite corners of a
rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers
to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by
doing the instructions Santa sent you in order.

For example:

    turn on 0,0 through 999,999 would turn on (or leave on) every light.

    toggle 0,0 through 999,0 would toggle the first line of 1000 lights,
    turning off the ones that were on, and turning on the ones that were off.

    turn off 499,499 through 500,500 would turn off (or leave off) the middle
    four lights.

After following the instructions, how many lights are lit?

Your puzzle answer was 400410.
--- Part Two ---

You just finish implementing your winning light pattern when you realize you
mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each
light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness of
those lights by 1.

The phrase turn off actually means that you should decrease the brightness of
those lights by 1, to a minimum of zero.

The phrase toggle actually means that you should increase the brightness of
those lights by 2.

What is the total brightness of all lights combined after following Santa's
instructions?

For example:

    turn on 0,0 through 0,0 would increase the total brightness by 1.

    toggle 0,0 through 999,999 would increase the total brightness by 2000000.

Your puzzle answer was 15343601.
"""
