from functools import partial
from tutils import (
    lmap,
    load_and_process_input,
    run_tests,
    splitstriplines,
)
from more_itertools import split_at
from toolz import sliding_window
import pdb

DAY = "01"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 24000
TA2 = None
ANSWER1 = None
ANSWER2 = None


def chunk(lines):
    return list(split_at(lines, lambda l: l == ""))


def process_one(data):
    max_cal = 0
    for snacks in data:
        total = sum(map(int, snacks))
        if total > max_cal:
            max_cal = total
    return max_cal


def process_two(data):
    top_three = [0, 0, 0]
    for snacks in data:
        total = sum(map(int, snacks))
        top_three = sorted(top_three)
        if total > top_three[0]:
            top_three[0] = total
    return sum(top_three)


def cli_main() -> None:
    input_funcs = [str.splitlines, chunk]
    data = load_and_process_input(INPUT, input_funcs)
    # data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    answer_one = process_one(data)
    print(answer_one)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    # answer_one = process_one(data)
    # assert answer_one == ANSWER1
    # print("Answer one:", answer_one)
    answer_two = process_two(data)
    print(answer_two)
    # assert answer_two == ANSWER2
    # print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
