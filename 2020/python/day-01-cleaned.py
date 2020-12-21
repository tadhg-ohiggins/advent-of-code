from functools import partial
from pathlib import Path
from typing import Any, Callable, List, Optional
from toolz import (  # type: ignore
    compose_left,
)

# pylint: disable=unsubscriptable-object
OInt = Optional[int]
# pylint: enable=unsubscriptable-object

lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lcompact = partial(lfilter, None)
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lstrip = partial(lmap, str.strip)
splitstriplines = compose_left(str.splitlines, lstrip, lcompact)


def load_and_process_input(fname: str, input_funcs: List[Callable]) -> Any:
    processinput = partial(process_input, input_funcs)
    return compose_left(load_input, processinput)(fname)


def process_input(input_funcs: List[Callable], text: str) -> Any:
    return compose_left(*input_funcs)(text)


def load_input(fname: str) -> str:
    return Path(fname).read_text().strip()


def tests(testfile: str, input_funcs: List[Callable]) -> Any:
    testdata = load_and_process_input(testfile, input_funcs)
    result = process_one(testdata)
    assert result == TESTANSWER_ONE
    print("Test answer one:", result)
    if ANSWER_ONE is not None:
        result_two = process_two(testdata)
        if TESTANSWER_TWO is not None:
            assert result_two == TESTANSWER_TWO
        print("Test answer two:", result_two)


def run_tests(testfile: str, input_funcs: List[Callable]) -> None:
    if Path(testfile).exists():
        tests(testfile, input_funcs)


""" END HELPER FUNCTIONS """


DAY = "01"
INPUT = f"input-{DAY}.txt"
TEST = f"test-input-{DAY}.txt"
TESTANSWER_ONE = 514579
TESTANSWER_TWO = 241861950
ANSWER_ONE = 357504
ANSWER_TWO = 12747392


def find_totals(target: int, array: List[int]) -> OInt:
    for item in array:
        if (target - item) in array:
            return (target - item) * item
    return None


def process_one(data: Any) -> Any:
    return find_totals(2020, data)


def process_two(data: Any) -> Any:
    for item in data:
        if result := find_totals(2020 - item, data):
            return result * item
    return None


def cli_main() -> None:
    input_funcs = [splitstriplines, partial(lmap, int)]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, input_funcs)
    answer_one = process_one(data)
    assert answer_one == ANSWER_ONE
    print("Answer one:", answer_one)
    answer_two = process_two(data)
    assert answer_two == ANSWER_TWO
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
"""
--- Day 1: Report Repair ---

After saving Christmas five years in a row, you've decided to take a vacation
at a nice resort on a tropical island. Surely, Christmas will go on without
you.

The tropical island has its own currency and is entirely cash-only. The gold
coins used there have a little picture of a starfish; the locals just call them
stars. None of the currency exchanges seem to have heard of them, but somehow,
you'll need to find fifty of these coins by the time you arrive so you can pay
the deposit on your room.

To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each
day in the Advent calendar; the second puzzle is unlocked when you complete the
first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense
report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then
multiply those two numbers together.

For example, suppose your expense report contained the following:

1721 979 366 299 675 1456

In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying
them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to
2020; what do you get if you multiply them together?

Your puzzle answer was 357504.

--- Part Two ---

The Elves in accounting are thankful for your help; one of them even offers you
a starfish coin they had left over from a past vacation. They offer you a
second one if you can find three numbers in your expense report that meet the
same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366,
and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to
2020?

Your puzzle answer was 12747392.
"""
