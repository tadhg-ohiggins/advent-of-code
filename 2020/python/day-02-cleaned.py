from functools import partial
from typing import List
from tutils import (
    lfilter,
    lmap,
    load_and_process_input,
    run_tests,
    splitstrip,
    splitstriplines,
)

DAY = "02"
INPUT = f"input-{DAY}.txt"
TEST = f"test-input-{DAY}.txt"
TA1 = 2
TA2 = 1
ANSWER1 = 424
ANSWER2 = 747


def line_to_rule(line: str) -> dict:
    rule, pw = splitstrip(line, ":")
    rule_range, rule_letter = splitstrip(rule)
    rule_min, rule_max = splitstrip(rule_range, "-")
    return {
        "pw": pw,
        "rule_letter": rule_letter,
        "rule_min": int(rule_min),
        "rule_max": int(rule_max),
    }


def is_valid_pw(item: dict) -> bool:
    pw, letter = item["pw"], item["rule_letter"]
    mn, mx = item["rule_min"], item["rule_max"]
    return mn <= pw.count(letter) <= mx


def is_valid_pw_two(item: dict) -> bool:
    pw, letter = item["pw"], item["rule_letter"]
    mn, mx = item["rule_min"], item["rule_max"]
    pos1, pos2 = pw[mn - 1], pw[mx - 1]
    return (letter in (pos1, pos2)) and pos1 != pos2


def process_one(data: List[dict]) -> int:
    return len(lfilter(is_valid_pw, data))


def process_two(data: List[dict]) -> int:
    return len(lfilter(is_valid_pw_two, data))


def cli_main() -> None:
    input_funcs = [splitstriplines, partial(lmap, line_to_rule)]
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
--- Day 2: Password Philosophy ---

Your flight departs in a few days from the coastal airport; the easiest way
down to the coast from here is via toboggan.

The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day.
"Something's wrong with our computers; we can't log in!" You ask if you can
take a look.

Their password database seems to be a little corrupted: some of the passwords
wouldn't have been allowed by the Official Toboggan Corporate Policy that was
in effect when they were chosen.

To try to debug the problem, they have created a list (your puzzle input) of
passwords (according to the corrupted database) and the corporate policy when
that password was set.

For example, suppose you have the following list:

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc

Each line gives the password policy and then the password. The password policy
indicates the lowest and highest number of times a given letter must appear for
the password to be valid. For example, 1-3 a means that the password must
contain a at least 1 time and at most 3 times.

In the above example, 2 passwords are valid. The middle password, cdefg, is
not; it contains no instances of b, but needs at least 1. The first and third
passwords are valid: they contain one a or nine c, both within the limits of
their respective policies.

How many passwords are valid according to their policies?

Your puzzle answer was 424.
--- Part Two ---

While it appears you validated the passwords correctly, they don't seem to be
what the Official Toboggan Corporate Authentication System is expecting.

The shopkeeper suddenly realizes that he just accidentally explained the
password policy rules from his old job at the sled rental place down the
street! The Official Toboggan Corporate Policy actually works a little
differently.

Each policy actually describes two positions in the password, where 1 means the
first character, 2 means the second character, and so on. (Be careful; Toboggan
Corporate Policies have no concept of "index zero"!) Exactly one of these
positions must contain the given letter. Other occurrences of the letter are
irrelevant for the purposes of policy enforcement.

Given the same example list from above:

    1-3 a: abcde is valid: position 1 contains a and position 3 does not.
    1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
    2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.

How many passwords are valid according to the new interpretation of the
policies?

Your puzzle answer was 747.
"""
