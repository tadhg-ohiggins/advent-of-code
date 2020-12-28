from functools import partial
from typing import List, cast
from toolz import sliding_window  # type: ignore
from tutils import (
    UBoolInt,
    lmap,
    load_and_process_input,
    nextwhere,
    run_tests,
    splitstriplines,
)

DAY = "09"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = None
TA2 = None
ANSWER1 = 104054607
ANSWER2 = 13935797


def do_two_items_sum_to(candidates: List[int], target: int) -> bool:
    return nextwhere(lambda num: target - num in candidates, candidates)


def is_not_sum_of_prior_n(numbers: List[int], limit: int) -> UBoolInt:
    """
    Shorter but less comprehensible:

    check = lambda item: not do_two_items_sum_to(item[:limit], item[limit])
    return nextwhere(check, sliding_window(limit + 1, numbers))
    """
    for window in sliding_window(limit + 1, numbers):
        candidates, target = window[:limit], window[limit]
        if not do_two_items_sum_to(candidates, target):
            return target
    return False


def find_range_that_sums_to(candidates: List[int], target: int) -> List:
    """
    The following line works, but is a lot slower than the for loop, probably
    because it has to keep the entire list of lists, whereas the for loop just
    has to keep the sum.
    return nextwhere(lambda x: sum(x) == target, list_accumulator(candidates))
    """
    total = 0
    for i, val in enumerate(candidates):
        total = total + val
        if total == target:
            return candidates[: i + 1]
    return []


def narrow_array(target: int, candidates: List[int]) -> UBoolInt:
    for i in range(len(candidates)):
        solution = find_range_that_sums_to(candidates[i:], target)
        if solution:
            solution = cast(List[int], solution)
            return min(solution) + max(solution)
    return False


def process_one(data: List[int]) -> UBoolInt:
    return is_not_sum_of_prior_n(data, 25)


def cli_main() -> None:
    input_funcs = [splitstriplines, partial(lmap, int)]
    data = load_and_process_input(INPUT, input_funcs)
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    process_two = partial(narrow_array, answer_one)
    # Can't run tests until after first half is solved because the second half
    # depends on the answer to the first half.
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_two = process_two(data)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
"""
--- Day 9: Encoding Error ---

With your neighbor happily enjoying their video game, you turn your attention
to an open data port on the little screen in the seat in front of you.

Though the port is non-standard, you manage to connect it to your computer
through the clever use of several paperclips. Upon connection, the port outputs
a series of numbers (your puzzle input).

The data appears to be encrypted with the eXchange-Masking Addition System
(XMAS) which, conveniently for you, is an old cypher with an important
weakness.

XMAS starts by transmitting a preamble of 25 numbers. After that, each number
you receive should be the sum of any two of the 25 immediately previous
numbers. The two numbers will have different values, and there might be more
than one such pair.

For example, suppose your preamble consists of the numbers 1 through 25 in a
random order. To be valid, the next number must be the sum of two of those
numbers:

    26 would be a valid next number, as it could be 1 plus 25 (or many other
    pairs, like 2 and 24).
    49 would be a valid next number, as it is the sum of 24 and 25.
    100 would not be valid; no two of the previous 25 numbers sum to 100.
    50 would also not be valid; although 25 appears in the previous 25 numbers,
    the two numbers in the pair must be different.

Suppose the 26th number is 45, and the first number (no longer an option, as it
is more than 25 numbers ago) was 20. Now, for the next number to be valid,
there needs to be some pair of numbers among 1-19, 21-25, or 45 that add up to
it:

    26 would still be a valid next number, as 1 and 25 are still within the
    previous 25 numbers.
    65 would not be valid, as no two of the available numbers sum to it.
    64 and 66 would both be valid, as they are the result of 19+45 and 21+45
    respectively.

Here is a larger example which only considers the previous 5 numbers (and has a
preamble of length 5):

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576

In this example, after the 5-number preamble, almost every number is the sum of
two of the previous 5 numbers; the only number that does not follow this rule
is 127.

The first step of attacking the weakness in the XMAS data is to find the first
number in the list (after the preamble) which is not the sum of two of the 25
numbers before it. What is the first number that does not have this property?

Your puzzle answer was 104054607.

--- Part Two ---

The final step in breaking the XMAS encryption relies on the invalid number you
just found: you must find a contiguous set of at least two numbers in your list
which sum to the invalid number from step 1.

Again consider the above example:

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576

In this list, adding up all of the numbers from 15 through 40 produces the
invalid number from step 1, 127. (Of course, the contiguous set of numbers in
your actual list might be much longer.)

To find the encryption weakness, add together the smallest and largest number
in this contiguous range; in this example, these are 15 and 47, producing 62.

What is the encryption weakness in your XMAS-encrypted list of numbers?

Your puzzle answer was 13935797.
"""
