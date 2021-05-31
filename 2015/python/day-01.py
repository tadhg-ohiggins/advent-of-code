from itertools import dropwhile
from operator import add
from tutils import Any
from tutils import accumulate
from tutils import load_and_process_input
from tutils import run_tests


""" END HELPER FUNCTIONS """


DAY = "01"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = None
TA2 = None
ANSWER1 = 74
ANSWER2 = 1795


def process_one(data: Any) -> int:
    plus = data.count("(")
    minus = data.count(")")
    return plus - minus


def process_two(data: Any) -> int:
    # Make string into list of numbers:
    def convert_to_numbers(char: str) -> int:
        return 1 if char == "(" else -1

    as_numbers = map(convert_to_numbers, data)

    # Add the numbers up to each spot in the list:
    added = accumulate(add, as_numbers)

    # Find the first instance of -1 and add 1 to its index since the floors are
    # 1-indexed:
    return next(dropwhile(lambda _: _[1] != -1, enumerate(added)))[0] + 1

    """
    floor = 0
    for i, char in enumerate(data):
        if char == "(":
            floor = floor + 1
        else:
            floor = floor - 1
        if floor == -1:
            # print(i + 1)
            break
    return i + 1
    """


def cli_main() -> None:
    input_funcs = [str.strip]
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


"""
--- Day 1: Not Quite Lisp ---

Santa was hoping for a white Christmas, but his weather machine's "snow"
function is powered by stars, and he's fresh out! To save Christmas, he needs
you to collect fifty stars by December 25th.

Collect stars by helping Santa solve puzzles. Two puzzles will be made
available on each day in the Advent calendar; the second puzzle is unlocked
when you complete the first. Each puzzle grants one star. Good luck!

Here's an easy puzzle to warm you up.

Santa is trying to deliver presents in a large apartment building, but he can't
find the right floor - the directions he got are a little confusing. He starts
on the ground floor (floor 0) and then follows the instructions one character
at a time.

An opening parenthesis, (, means he should go up one floor, and a closing
parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he will
never find the top or bottom floors.

For example:

    (()) and ()() both result in floor 0.
    ((( and (()(()( both result in floor 3.
    ))((((( also results in floor 3.
    ()) and ))( both result in floor -1 (the first basement level).
    ))) and )())()) both result in floor -3.

To what floor do the instructions take Santa?

Your puzzle answer was 74.
--- Part Two ---

Now, given the same instructions, find the position of the first character that
causes him to enter the basement (floor -1). The first character in the
instructions has position 1, the second character has position 2, and so on.

For example:

    ) causes him to enter the basement at character position 1.
    ()()) causes him to enter the basement at character position 5.

What is the position of the character that causes Santa to first enter the
basement?

Your puzzle answer was 1795.
"""
