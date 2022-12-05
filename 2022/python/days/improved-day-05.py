from functools import reduce
import re
from toolz import pipe
from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    lfilter,  # A version of filter that returns a list.
    lmap,  # A version of map that returns a list.
    splitstriplines,
)


TEST_ANSWERS = ("CMZ", "MCD")
PUZZLE_ANSWERS = ("JDTMRWCQJ", "VHJDDCWRD")


def parse_state_and_moves(data):
    return get_initial_state(data[0]), get_moves(data[1])


def get_crates(lines, position):
    start, end = position.span()
    return lfilter(None, (line[start:end].strip() for line in lines))


def get_initial_state(text):
    lines = text.splitlines()
    positions = list(re.finditer(r"\d+", lines[-1]))
    stacks = lines[:-1][::-1]
    return {int(pos.group()): get_crates(stacks, pos) for pos in positions}


def get_moves(text):
    def triple(line):
        return lmap(int, re.findall(r"\d+", line))

    return pipe(text, splitstriplines, cmap(triple))


def make_move(state, num, origin, destination):
    reducer = lambda acc, _: make_move_multi(acc, 1, origin, destination)
    return reduce(reducer, range(num), state)


def make_move_multi(state, num, origin, destination):
    return state | {
        origin: state[origin][:-num],
        destination: state[destination] + state[origin][-num:],
    }


def preprocess(data):
    return data.split("\n\n")


def part_one(data):
    state, moves = parse_state_and_moves(data)
    update = reduce(lambda acc, m: make_move(acc, *m), moves, state)
    return "".join([update[k][-1] for k in update])


def part_two(data):
    state, moves = parse_state_and_moves(data)
    update = reduce(lambda acc, m: make_move_multi(acc, *m), moves, state)
    return "".join([update[k][-1] for k in update])
