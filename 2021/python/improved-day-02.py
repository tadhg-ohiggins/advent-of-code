from functools import partial
import pdb
import aoc
from tadhg_utils import (
    c_lmap,
    lmap,
    splitstriplines,
)


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 150
TA2 = 900
A1 = 2102357
A2 = 2101031224


def parse_line(line):
    command, incr = line.split(" ")
    return command, int(incr)


def parse_lines(lines):
    return lmap(parse_line, lines)


def process_one(data):
    horiz, depth = 0, 0
    for command, incr in data:
        if command == "forward":
            horiz = horiz + incr
        elif command == "down":
            depth = depth + incr
        elif command == "up":
            depth = depth - incr

    return horiz * depth


def process_two(data):
    horiz, depth, aim = 0, 0, 0
    for command, incr in data:
        if command == "forward":
            horiz = horiz + incr
            depth = depth + (aim * incr)
        elif command == "down":
            aim = aim + incr
        elif command == "up":
            aim = aim - incr
    return depth * horiz


def cli_main() -> None:
    input_funcs = [splitstriplines, parse_lines]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    result_two = process_two(data)
    try:
        if A1 is not None:
            assert result_one == A1
        print("Answer one:", result_one)
        if A2 is not None:
            assert result_two == A2
        print("Answer two:", result_two)
    except AssertionError:
        pdb.set_trace()


if __name__ == "__main__":
    cli_main()
