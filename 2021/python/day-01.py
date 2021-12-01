from functools import partial
from tutils import (
    lmap,
    load_and_process_input,
    run_tests,
    splitstriplines,
)
from toolz import sliding_window
import pdb

DAY = "01"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = None
TA2 = None
ANSWER1 = None
ANSWER2 = None


def process_one(data):
    current = 0
    count = 0
    for i in data:
        if i > current:
            count = count + 1
        current = i
    return count - 1


def process_two(data):
    current = 0
    count = 0
    for sw in sliding_window(3, data):
        swsum = sum(sw)
        if swsum > current:
            count = count + 1
        current = swsum
    return count - 1


def cli_main() -> None:
    input_funcs = [splitstriplines, partial(lmap, int)]
    data = load_and_process_input(INPUT, input_funcs)
    # data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    answer_one = process_one(data)
    print(answer_one)
    # run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    # answer_one = process_one(data)
    # assert answer_one == ANSWER1
    # print("Answer one:", answer_one)
    answer_two = process_two(data)
    print(answer_two)
    # assert answer_two == ANSWER2
    # print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
