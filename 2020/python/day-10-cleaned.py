from __future__ import annotations
from collections import Counter
from functools import partial, reduce
from typing import List
from toolz import sliding_window  # type: ignore
from tutils import (
    lmap,
    load_and_process_input,
    lnoncontinuous,
    run_tests,
    splitstriplines,
)

DAY = "10"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 220
TA2 = 19208
ANSWER1 = 2272
ANSWER2 = 84627647627264


def find_combos(length: int) -> int:
    """
    In the data, there are no gaps of two, only gaps of one or three, between
    numbers in the sorted list.
    The rules are such that the number of combos are the same regardless
    of the specific numbers involved--there are the same number of combos
    for [0, 1, 2, 3] and for [23, 24, 25, 26].
    So we only need the length of a run to figure out the number of
    combos in it.

    The rule is that any number can be skipped as long as there's not a gap of
    more than three. Since we're dealing with runs that are separated by gaps
    of three, the first and last numbers must be included in each combo.

    So for [0, 1, 2] the only combos are [0, 2] and [0, 1, 2].

    For runs of three, the answer is two. For four, it's four. But at five, you
    hit a limit of having a gap of more than three between the start and
    finish.

    Because the start and finish numbers of each run are required, and gaps of
    more than three aren't allowed, and there are no gaps of two, it looks like
    a run of n has combos equal to the sum of runs of n-1, n-2, n-3.

    n1 = 1
    n2 = 1
    n3 = 2
    n4 = 4
    n5 = 7
    n6 = 13
    """

    start = {0: 0, 1: 1, 2: 1}
    if length in start:
        return start[length]
    return sum(map(find_combos, [max([0, length - _]) for _ in (1, 2, 3)]))


def incl_ends(adapters: List[int]) -> List[int]:
    return sorted([0] + adapters + [max(adapters) + 3])


def process_one(adapters: List[int]) -> int:
    diffs = Counter([a - b for a, b in sliding_window(2, reversed(adapters))])
    return diffs[1] * diffs[3]


def process_two(adapters: List[int]) -> int:
    runs = Counter([len(span) for span in lnoncontinuous(adapters)])
    combos = {k: find_combos(k) for k in runs}
    return reduce(lambda n, c: n * combos[c] ** runs[c], combos, 1)


def cli_main() -> None:
    input_funcs = [splitstriplines, partial(lmap, int), incl_ends]
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
