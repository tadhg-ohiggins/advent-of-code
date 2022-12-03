from functools import partial
from toolz import pipe
from toolz.curried import get, map as cmap
from tutils import (
    innermap,
    lfilter,
    lmap,
    load_and_process_input,
    run_tests,
    splitblocks,
    splitstriplines,
)

TEST_ANSWERS = (15, 12)
PUZZLE_ANSWERS = (13268, 15508)

RESP = {"A": "X", "B": "Y", "C": "Z"}


def get_result(pair):
    if pair[0] == "A" and pair[1] == "X":
        return 3
    if pair[0] == "A" and pair[1] == "Y":
        return 6
    if pair[0] == "A" and pair[1] == "Z":
        return 0
    if pair[0] == "B" and pair[1] == "X":
        return 0
    if pair[0] == "B" and pair[1] == "Y":
        return 3
    if pair[0] == "B" and pair[1] == "Z":
        return 6
    if pair[0] == "C" and pair[1] == "X":
        return 6
    if pair[0] == "C" and pair[1] == "Y":
        return 0
    if pair[0] == "C" and pair[1] == "Z":
        return 3


def shape_score(shape):
    return {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }[shape]


def get_winpair(pair):
    if pair[0] == "A" and pair[1] == "X":
        return ["A", "Z"]
    if pair[0] == "A" and pair[1] == "Y":
        return ["A", "X"]
    if pair[0] == "A" and pair[1] == "Z":
        return ["A", "Y"]
    if pair[0] == "B" and pair[1] == "X":
        return ["B", "X"]
    if pair[0] == "B" and pair[1] == "Y":
        return ["B", "Y"]
    if pair[0] == "B" and pair[1] == "Z":
        return pair
    if pair[0] == "C" and pair[1] == "X":
        return ["C", "Y"]
    if pair[0] == "C" and pair[1] == "Y":
        return ["C", "Z"]
    if pair[0] == "C" and pair[1] == "Z":
        return ["C", "X"]


def get_score(pair):
    return get_result(pair) + shape_score(pair[1])


def preprocess(data):
    procs = [splitstriplines, partial(lmap, str.split)]
    result = pipe(data, *procs)
    return result


def part_one(data):
    procs = [cmap(get_score), sum]
    result = pipe(data, *procs)
    return result


def part_two(data):
    procs = [cmap(get_winpair), cmap(get_score), sum]
    result = pipe(data, *procs)
    return result
