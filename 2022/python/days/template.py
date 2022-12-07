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


TEST_ANSWERS = (None, None)
PUZZLE_ANSWERS = (None, None)


def all_diff(seq):
    return len(seq) == len(set(seq))


def preprocess(data):
    procs = [
        str.strip,
        trace,
    ]
    result = pipe(data, *procs)
    return result


def part_one(data):
    procs = [
        trace,
    ]
    result = pipe(data, *procs)
    return result


def part_two(data):
    procs = [
        trace,
    ]
    result = pipe(data, *procs)
    return result
