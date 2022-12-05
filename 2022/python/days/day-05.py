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


TEST_ANSWERS = ("CMZ", "MCD")
PUZZLE_ANSWERS = ("JDTMRWCQJ", "VHJDDCWRD")


def get_initial_state(text):
    lines = text.splitlines()
    positions = list(re.finditer(r"\d+", lines[-1]))
    state = {}
    # rightmost position in list is topmost position in diagram.
    for position in positions:
        key = int(position.group())
        start, end = position.span()
        for line in lines[:-1][::-1]:
            value = line[start:end]
            if key not in state and value.strip():
                state[key] = [value]
            elif value.strip():
                state[key].append(value)
    return state


def get_moves(text):
    def triple(line):
        return lmap(int, re.findall(r"\d+", line))

    lines = splitstriplines(text)

    return lmap(triple, lines)


def make_move(state, num, origin, destination):
    for _ in range(num):
        value = state[origin].pop()
        state[destination].append(value)
    return state


def make_move_multi(state, num, origin, destination):
    if num == 1:
        return make_move(state, num, origin, destination)

    neworigin, tomove = state[origin][:-num], state[origin][-num:]
    state[origin] = neworigin
    state[destination] = state[destination] + tomove
    return state


def preprocess(data):
    procs = (lambda t: t.split("\n\n"),)
    result = pipe(data, *procs)
    return result


def part_one(data):
    state = get_initial_state(data[0])
    moves = get_moves(data[1])
    for move in moves:
        state = make_move(state, *move)

    result = "".join([state[k][-1] for k in state])
    return result


def part_two(data):
    state = get_initial_state(data[0])
    moves = get_moves(data[1])
    for move in moves:
        state = make_move_multi(state, *move)

    result = "".join([state[k][-1] for k in state])
    return result
