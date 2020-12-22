from functools import partial
from typing import List
from tutils import (
    lfilter,
    lmap,
    load_and_process_input,
    run_tests,
    splitstriplines,
)

DAY = "06"
INPUT = f"input-{DAY}.txt"
TEST = f"test-input-{DAY}.txt"
TA1 = None
TA2 = None
ANSWER1 = 6903
ANSWER2 = 3493


def group_to_unanimous(group: List[str]) -> int:
    check = lambda char: all([char in line for line in group])
    return len(lfilter(check, set("".join(group))))


def process_one(groups: List[List[str]]) -> int:
    return sum([len(set("".join(group))) for group in groups])


def process_two(groups: List[List[str]]) -> int:
    return sum(map(group_to_unanimous, groups))


def cli_main() -> None:
    input_funcs = [
        partial(str.split, sep="\n\n"),
        partial(lmap, splitstriplines),
    ]
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
--- Day 6: Custom Customs ---

As your flight approaches the regional airport where you'll switch to a much
larger plane, customs declaration forms are distributed to the passengers.

The form asks a series of 26 yes-or-no questions marked a through z. All you
need to do is identify the questions for which anyone in your group answers
"yes". Since your group is just you, this doesn't take very long.

However, the person sitting next to you seems to be experiencing a language
barrier and asks if you can help. For each of the people in their group, you
write down the questions for which they answer "yes", one per line. For
example:

abcx
abcy
abcz

In this group, there are 6 questions to which anyone answered "yes": a, b, c,
x, y, and z. (Duplicate answers to the same question don't count extra; each
question counts at most once.)

Another group asks for your help, then another, and eventually you've collected
answers from every group on the plane (your puzzle input). Each group's answers
are separated by a blank line, and within each group, each person's answers are
on a single line. For example:

abc

a
b
c

ab
ac

a
a
a
a

b

This list represents answers from five groups:

    The first group contains one person who answered "yes" to 3 questions: a,
    b, and c.
    The second group contains three people; combined, they answered "yes" to 3
    questions: a, b, and c.
    The third group contains two people; combined, they answered "yes" to 3
    questions: a, b, and c.
    The fourth group contains four people; combined, they answered "yes" to
    only 1 question, a.
    The last group contains one person who answered "yes" to only 1 question,
    b.

In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.

For each group, count the number of questions to which anyone answered "yes".
What is the sum of those counts?

Your puzzle answer was 6903.

--- Part Two ---

As you finish the last group's customs declaration, you notice that you misread
one word in the instructions:

You don't need to identify the questions to which anyone answered "yes"; you
need to identify the questions to which everyone answered "yes"!

Using the same example as above:

abc

a
b
c

ab
ac

a
a
a
a

b

This list represents answers from five groups:

    In the first group, everyone (all 1 person) answered "yes" to 3 questions:
        a, b, and c.
    In the second group, there is no question to which everyone answered "yes".
    In the third group, everyone answered yes to only 1 question, a. Since some
    people did not answer "yes" to b or c, they don't count.
    In the fourth group, everyone answered yes to only 1 question, a.
    In the fifth group, everyone (all 1 person) answered "yes" to 1 question,
    b.

In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.

For each group, count the number of questions to which everyone answered "yes".
What is the sum of those counts?

Your puzzle answer was 3493.
"""
