from functools import cache, partial, reduce
from itertools import permutations
from operator import itemgetter
from string import ascii_lowercase, ascii_uppercase
from tadhg_utils import (
    p_lmap as cmap,  # Curried version of map that return a list.
    lmap,  # A version of map that returns a list.
    splitstrip,
    splitstriplines,
)
from more_itertools import chunked
from toolz import compose_left, curry, pipe, sliding_window
import pdb


TEST_ANSWERS = (None, None)
PUZZLE_ANSWERS = (141, 736)


# Preprocessing:


def to_triplet(line):
    line = line.replace(" to ", " = ")
    city1, city2, distance = splitstrip(line, sep=" = ")
    return (city1, city2, int(distance))


def triplet_to_dict(triplet):
    return {(triplet[0], triplet[1]): triplet[2]}


def combine(dicts):
    return reduce(lambda a, d: a | d, dicts, {})


def add_reverse(routes):
    def rev(d):
        return {(k[1], k[0]): v for k, v in d.items()}

    return routes | rev(routes)


# Distances:


def all_cities(pairs):
    return set(reduce(lambda a, t: a + [t[0], t[1]], pairs, []))


def get_distance(scores, path):
    procs = (
        partial(sliding_window, 2),
        list,
        cmap(scores.get),
        sum,
    )
    return pipe(path, *procs)


def get_distances(data):
    procs = (
        dict.keys,
        list,
        all_cities,
        permutations,
        list,
        cmap(partial(get_distance, data)),
        sorted,
    )
    return pipe(data, *procs)


def preprocess(data):
    procs = [
        splitstriplines,
        cmap(to_triplet),
        cmap(triplet_to_dict),
        combine,
        add_reverse,
    ]
    result = pipe(data, *procs)
    return result


def part_one(data):
    routes = get_distances(data)
    return routes[0]


def part_two(data):
    routes = get_distances(data)
    return routes[-1]
