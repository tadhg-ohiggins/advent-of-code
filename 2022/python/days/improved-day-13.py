from ast import literal_eval
from functools import cmp_to_key
from itertools import chain

from tutils import splitblocks
from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    splitstriplines,
)


TEST_ANSWERS = (13, 140)
PUZZLE_ANSWERS = (5557, 22425)


def eval_block(block):
    return cmap(literal_eval)(splitstriplines(block))


def preprocess(data):
    return cmap(eval_block)(splitblocks(data))


def sort_pair(item_one, item_two):
    if isinstance(item_one, int) and isinstance(item_two, int):
        return item_one - item_two

    if isinstance(item_one, list) and isinstance(item_two, list):
        for item in zip(item_one, item_two):
            if (comparison := sort_pair(*item)) != 0:
                return comparison

        return len(item_one) - len(item_two)

    if isinstance(item_one, list) and isinstance(item_two, int):
        return sort_pair(item_one, [item_two])
    # if isinstance(item_one, int) and isinstance(item_two, list):
    return sort_pair([item_one], item_two)


def part_one(pairs):
    return sum(i + 1 for i, p in enumerate(pairs) if sort_pair(*p) < 0)


def part_two(pairs):
    singles = list(chain.from_iterable(pairs)) + [[[2]], [[6]]]
    ordered = sorted(singles, key=cmp_to_key(sort_pair))
    return (1 + ordered.index([[2]])) * (1 + ordered.index([[6]]))
