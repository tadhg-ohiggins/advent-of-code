from more_itertools import split_at
from toolz import pipe


TEST_ANSWERS = (24000, 45000)
PUZZLE_ANSWERS = (69206, 197400)


def chunk(lines):
    return list(split_at(lines, lambda l: l == ""))


def preprocess(data):
    return pipe(data, *(str.splitlines, chunk))


def part_one(data):
    max_cal = 0
    for snacks in data:
        total = sum(map(int, snacks))
        if total > max_cal:
            max_cal = total
    return max_cal


def part_two(data):
    top_three = [0, 0, 0]
    for snacks in data:
        total = sum(map(int, snacks))
        top_three = sorted(top_three)
        if total > top_three[0]:
            top_three[0] = total
    return sum(top_three)
