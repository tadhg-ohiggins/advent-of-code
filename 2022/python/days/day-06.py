from functools import partial
from itertools import permutations
from string import ascii_lowercase, ascii_uppercase
import re

from more_itertools import chunked
from toolz import (
    compose_left,
    pipe,
    sliding_window,
)

from tutils import trace, splitblocks
from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    lfilter,
    lmap,  # A version of map that returns a list.
    splitstriplines,
    splitstrip,
    star,
)
import pdb


TEST_ANSWERS = (7, 19)
PUZZLE_ANSWERS = (1582, 3588)


def all_diff(seq):
    return len(seq) == len(set(seq))


def preprocess(data):
    procs = (lambda t: t.strip(),)
    result = pipe(data, *procs)
    return result


def part_one(data):
    procs = (
        partial(sliding_window, 4),
        list,
    )

    result = pipe(data, *procs)
    first = ""
    for seq in result:
        if all_diff(seq):
            first = "".join(seq)
            break
    pos = list(re.finditer(first, data))[0]
    return pos.span()[1]


def part_two(data):
    procs = (
        partial(sliding_window, 14),
        list,
    )

    result = pipe(data, *procs)
    first = ""
    for seq in result:
        if all_diff(seq):
            first = "".join(seq)
            break
    pos = list(re.finditer(first, data))[0]
    return pos.span()[1]
