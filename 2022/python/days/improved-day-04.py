from functools import partial
from operator import itemgetter
from toolz import pipe
from tadhg_utils import (
    p_lmap as cmap,  # Partial/curried map that returns a list.
    lfilter,  # filter that returns a list
    splitstriplines,
    splitstrip,
)

TEST_ANSWERS = (2, 4)
PUZZLE_ANSWERS = (567, 907)


def get_range_ends(pair):
    procs = (
        cmap(partial(splitstrip, sep="-")),
        cmap(cmap(int)),
    )
    return pipe(pair, *procs)


def is_contained(pair):
    a, b, x, y = pair[0] + pair[1]
    return (a <= x and b >= y) or (a >= x and b <= y)


def is_partly_contained(pair):
    a, b, x, y = pair[0] + pair[1]
    return a <= y and b >= x


def preprocess(data):
    procs = [
        splitstriplines,
        cmap(partial(splitstrip, sep=",")),
        cmap(get_range_ends),
    ]
    return pipe(data, *procs)


def part_one(data):
    procs = (
        partial(sorted, key=itemgetter(0)),
        cmap(is_contained),
        partial(lfilter, None),
        len,
    )
    return pipe(data, *procs)


def part_two(data):
    procs = (
        partial(sorted, key=itemgetter(0)),
        cmap(is_partly_contained),
        partial(lfilter, None),
        len,
    )
    return pipe(data, *procs)
