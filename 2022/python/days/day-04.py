from functools import partial
from string import ascii_lowercase, ascii_uppercase
from tutils import (
    c_lmap as cmap,  # Curried version of map that return a list.
    dpipe,  # Adds set_trace to every function in the function list of pipe.
    lmap,  # A version of map that returns a list.
    splitstriplines,
    splitstrip,
    trace,
)
from more_itertools import chunked
from toolz import compose_left, pipe
from tadhg_utils import lfilter, star
import pdb


TEST_ANSWERS = (2, 4)
PUZZLE_ANSWERS = (567, 907)


def get_range(pair):
    separated = lmap(partial(splitstrip, sep="-"), pair)
    return lmap(cmap(int), separated)


def preprocess(data):
    procs = [
        splitstriplines,
        cmap(partial(splitstrip, sep=",")),
        cmap(get_range),
    ]
    result = pipe(data, *procs)
    return result


def is_contained(pair):
    adj = [[pair[0][0], pair[0][1] + 1], [pair[1][0], pair[1][1] + 1]]
    ranges = lmap(star(range), adj)
    lranges = lmap(list, ranges)
    sranges = sorted(lranges, key=len)
    return all(x in sranges[1] for x in sranges[0])


def is_partly_contained(pair):
    adj = [[pair[0][0], pair[0][1] + 1], [pair[1][0], pair[1][1] + 1]]
    ranges = lmap(star(range), adj)
    lranges = lmap(list, ranges)
    sranges = sorted(lranges, key=len)
    return any(x in sranges[1] for x in sranges[0])


def part_one(data):
    procs = [cmap(is_contained), partial(lfilter, None), len]
    result = pipe(data, *procs)
    return result


def part_two(data):
    procs = [cmap(is_partly_contained), partial(lfilter, None), len]
    result = pipe(data, *procs)
    return result
