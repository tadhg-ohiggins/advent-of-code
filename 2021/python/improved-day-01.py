from functools import partial
from tutils import (
    lfilter,
    lmap,
    load_and_process_input,
    run_tests,
    splitstriplines,
)
from toolz import sliding_window  # type: ignore

DAY = "01"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 7
TA2 = 5
ANSWER1 = 1602
ANSWER2 = 1633


def comparer(pair: tuple[int, int]) -> bool:
    return pair[1] > pair[0]


def process_one(data: list[int]) -> int:
    return len(lfilter(comparer, sliding_window(2, data)))


def process_two(data: list[int]) -> int:
    totals = map(sum, sliding_window(3, data))
    return len(lfilter(comparer, sliding_window(2, totals)))


def cli_main() -> None:
    input_funcs = [splitstriplines, partial(lmap, int)]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process_two(data)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
