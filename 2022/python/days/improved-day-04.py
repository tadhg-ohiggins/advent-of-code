from functools import partial
from operator import methodcaller
from toolz import compose_left, pipe
from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable map that returns a list.
    lcompact,  # filter(None) that returns a list.
    splitstriplines,
    star,  # Changes function so that star(func)(arg) == func(*arg).
)

TEST_ANSWERS = (2, 4)
PUZZLE_ANSWERS = (567, 907)


def get_ints(line):
    procs = (
        methodcaller("replace", "-", ","),
        methodcaller("split", ","),
        cmap(int),
    )
    return pipe(line, *procs)


def is_contained(a, b, x, y):
    return (a <= x and b >= y) or (a >= x and b <= y)


def is_partly_contained(a, b, x, y):
    return a <= y and b >= x


preprocess = compose_left(
    splitstriplines,
    cmap(get_ints),
)

part_one = compose_left(
    cmap(star(is_contained)),
    lcompact,
    len,
)

part_two = compose_left(
    cmap(star(is_partly_contained)),
    lcompact,
    len,
)
