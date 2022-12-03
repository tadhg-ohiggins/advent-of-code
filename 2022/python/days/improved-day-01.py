from functools import partial
from toolz import pipe
from toolz.curried import get, map as cmap
from tutils import (
    innermap,
    splitblocks,
    splitstriplines,
)


TEST_ANSWERS = (24000, 45000)
PUZZLE_ANSWERS = (69206, 197400)


def preprocess(data):
    procs = (splitblocks, cmap(splitstriplines), partial(innermap, int))
    return pipe(data, *procs)


def part_one(data):
    return pipe(data, *(cmap(sum), sorted))[-1]


def part_two(data):
    return pipe(data, *(cmap(sum), sorted, get([-1, -2, -3]), sum))
