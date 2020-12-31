from functools import partial
from itertools import count
from typing import List
from tutils import lmap, splitstrip, load_and_process_input

DAY = "15"
INPUT = f"input-{DAY}.txt"
ANSWER1 = 240
ANSWER2 = 505
testdata = [
    ([0, 3, 6], 2020, 436),
    ([1, 3, 2], 2020, 1),
    ([2, 1, 3], 2020, 10),
    ([1, 2, 3], 2020, 27),
    ([2, 3, 1], 2020, 78),
    ([3, 2, 1], 2020, 438),
    ([3, 1, 2], 2020, 1836),
]


def find_nth_number(numbers: List[int], ordinal: int) -> int:
    positions = {x: i for i, x in enumerate(numbers)}
    for index in count(len(numbers) - 1):
        current = numbers[index]
        lastpos = positions.get(current, False)
        positions[current] = index
        steps_back = 0 if lastpos is False else index - lastpos

        numbers.append(steps_back)

        if len(numbers) == ordinal:
            break
    return steps_back


def process(numbers: List[int], ordinal: int) -> int:
    return find_nth_number(numbers, ordinal)


def cli_main() -> None:
    input_funcs = [
        partial(str.strip),
        partial(splitstrip, sep=","),
        partial(lmap, int),
    ]
    numbers = load_and_process_input(INPUT, input_funcs)
    for nums, ordinal, tanswer in testdata:
        testanswer = find_nth_number(nums, ordinal)
        assert testanswer == tanswer
    answer_one = process(numbers[:], 2020)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process(numbers[:], 30000000)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
