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
TA2 = 45000
ANSWER1 = 69206
ANSWER2 = 197400


def chunk(lines):
    return lmap(partial(lmap, int), (split_at(lines, lambda l: l == "")))


def process_one(data):
    totals = lmap(sum, data)
    return sorted(totals)[-1]


def process_two(data):
    totals = lmap(sum, data)
    return sum(sorted(totals)[-3:])


def cli_main() -> None:
    input_funcs = [str.splitlines, chunk]
    data = load_and_process_input(INPUT, input_funcs)
    answer_one = process_one(data)
    # print(answer_one)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process_two(data)
    print(answer_two)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
