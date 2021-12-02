from functools import partial
from tutils import (
    lmap,
    load_and_process_input,
    run_tests,
    splitstriplines,
)
from toolz import sliding_window
import pdb

DAY = "02"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 150
TA2 = 900
ANSWER1 = 2102357
ANSWER2 = 2101031224


def process_one(data):
    horiz = 0
    depth = 0
    for line in data:
        command, strincr = line.split(" ")
        incr = int(strincr)
        if command == "forward":
            horiz = horiz + incr
        elif command == "down":
            depth = depth + incr
        elif command == "up":
            depth = depth - incr

    return horiz * depth


def process_two(data):
    horiz = 0
    depth = 0
    aim = 0
    for line in data:
        command, strincr = line.split(" ")
        incr = int(strincr)
        if command == "forward":
            horiz = horiz + incr
            depth = depth + (aim * incr)
        elif command == "down":
            aim = aim + incr
        elif command == "up":
            aim = aim - incr
    return depth * horiz


def cli_main() -> None:
    input_funcs = [splitstriplines]
    data = load_and_process_input(INPUT, input_funcs)
    # data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    answer_one = process_one(data)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_two = process_two(data)
    try:
        if ANSWER1 is not None:
            assert answer_one == ANSWER1
        print("Answer one:", answer_one)
        if ANSWER1 is not None:
            answer_two = process_two(data)
            print(answer_two)
        if ANSWER2 is not None:
            assert answer_two == ANSWER2
    except AssertionError as e:
        pdb.set_trace()
    # print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
