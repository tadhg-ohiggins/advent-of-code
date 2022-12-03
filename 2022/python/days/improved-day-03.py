from string import ascii_lowercase, ascii_uppercase
from more_itertools import chunked, divide
from toolz import pipe
from tutils import c_lmap as cmap, lmap, splitstriplines
from tadhg_utils import star


TEST_ANSWERS = (157, 70)
PUZZLE_ANSWERS = (8053, 2425)


def chunk(items):
    return list(chunked(items, 3))


def letterscore(letter):
    return 1 + (ascii_lowercase + ascii_uppercase).index(letter)


def twosplit(line):
    return lmap(list, divide(2, line))


def get_common(group):
    return pipe(group, *(cmap(set), star(set.intersection), set.pop))


def preprocess(data):
    return splitstriplines(data)


def part_one(data):
    procs = [cmap(twosplit), cmap(get_common), cmap(letterscore), sum]
    return pipe(data, *procs)


def part_two(data):
    procs = [chunk, cmap(get_common), cmap(letterscore), sum]
    return pipe(data, *procs)
