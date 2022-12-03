from functools import partial
from tutils import (
    c_lmap as cmap,
    lmap,
    splitstriplines,
)
from more_itertools import chunked
from toolz import pipe
from string import ascii_lowercase, ascii_uppercase
import pdb


TEST_ANSWERS = (157, 70)
PUZZLE_ANSWERS = (8053, 2425)


def chunk(items):
    return list(chunked(items, 3))


def get_three(group):
    common = [_ for _ in group[0] if _ in group[1] and _ in group[2]]
    return list(set(common))[0]


def letterscore(letter):
    if letter in ascii_lowercase:
        return ascii_lowercase.index(letter) + 1
    return ascii_uppercase.index(letter) + 27


def twosplit(line):
    half = len(line) // 2
    return [line[:half], line[half:]]


def get_common(pair):
    return list(set([_ for _ in pair[0] if _ in pair[1]]))[0]


def preprocess(data):
    procs = [splitstriplines]
    result = pipe(data, *procs)
    return result


def part_one(data):
    procs = [cmap(twosplit), cmap(get_common), cmap(letterscore), sum]
    result = pipe(data, *procs)
    return result


def part_two(data):
    procs = [chunk, cmap(get_three), cmap(letterscore), sum]
    result = pipe(data, *procs)
    return result
