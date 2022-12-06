from itertools import dropwhile
import re
from toolz import first, sliding_window

TEST_ANSWERS = (7, 19)
PUZZLE_ANSWERS = (1582, 3588)


def find_qual(seqs):
    not_all_diff = lambda seq: len(seq) != len(set(seq))
    return first(dropwhile(not_all_diff, seqs))


def find_last_char_of_first_unique(data, sequences):
    start = "".join(find_qual(sequences))
    return re.search(start, data).span()[-1]


def preprocess(data):
    return data.strip()


def part_one(data):
    windows = sliding_window(4, data)
    return find_last_char_of_first_unique(data, windows)


def part_two(data):
    windows = sliding_window(14, data)
    return find_last_char_of_first_unique(data, windows)
