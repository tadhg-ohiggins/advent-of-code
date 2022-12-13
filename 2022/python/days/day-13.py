from functools import cmp_to_key, partial
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


TEST_ANSWERS = (13, 140)
PUZZLE_ANSWERS = (5557, 22425)


def eval_block(block):
    return lmap(eval, splitstriplines(block))


def preprocess(data):
    procs = [
        splitblocks,
        cmap(eval_block),
    ]
    result = pipe(data, *procs)
    return result


def compare_pair(item_one, item_two):
    if isinstance(item_one, int) and isinstance(item_two, int):
        if item_one == item_two:
            return "Tie"
        if item_one < item_two:
            return True
        return False
    else:
        if isinstance(item_one, list) and isinstance(item_two, int):
            return compare_pair(item_one, [item_two])
        if isinstance(item_one, int) and isinstance(item_two, list):
            return compare_pair([item_one], item_two)
        if isinstance(item_one, list) and isinstance(item_two, list):
            both = zip(item_one, item_two)
            if len(item_one) < len(item_two):
                stopiter = True
            elif len(item_one) > len(item_two):
                stopiter = False
            else:
                stopiter = "Tie"
            sentinel = object()
            while both:
                item = next(both, sentinel)
                if item == sentinel:
                    return stopiter
                curr = compare_pair(*item)
                if curr == "Tie":
                    continue
                return curr


def sort_pair(item_one, item_two):
    if isinstance(item_one, int) and isinstance(item_two, int):
        if item_one == item_two:
            return 0
        if item_one < item_two:
            return -1
        return 1
    else:
        if isinstance(item_one, list) and isinstance(item_two, int):
            return sort_pair(item_one, [item_two])
        if isinstance(item_one, int) and isinstance(item_two, list):
            return sort_pair([item_one], item_two)
        if isinstance(item_one, list) and isinstance(item_two, list):
            both = zip(item_one, item_two)
            # import pdb
            #
            # pdb.set_trace()
            if len(item_one) < len(item_two):
                stopiter = -1
            elif len(item_one) > len(item_two):
                stopiter = 1
            else:
                stopiter = 0
            sentinel = object()
            while both:
                item = next(both, sentinel)
                if item == sentinel:
                    return stopiter
                curr = sort_pair(*item)
                if curr == 0:
                    continue
                return curr


def part_one(pairs):
    results = []
    for i, items in enumerate(pairs):
        if compare_pair(*items):
            results.append(i + 1)
    return sum(results)


def part_two(pairs):
    singles = []
    for one, two in pairs:
        singles.append(one)
        singles.append(two)

    singles = singles + [
        [[2]],
        [[6]],
    ]

    ordered = sorted(singles, key=cmp_to_key(sort_pair))
    return (1 + ordered.index([[2]])) * (1 + ordered.index([[6]]))
