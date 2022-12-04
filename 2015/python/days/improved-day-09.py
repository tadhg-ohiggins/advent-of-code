from functools import partial, reduce
from itertools import chain, permutations
from tadhg_utils import (
    p_lmap as cmap,  # Curried version of map that return a list.
    multireplace,
    splitstrip,
    splitstriplines,
)
from toolz import pipe, sliding_window  # type: ignore


TEST_ANSWERS = (None, None)
PUZZLE_ANSWERS = (141, 736)


# Preprocessing:


def to_dict(line: str) -> dict:
    stripped = multireplace(("to", "="), "", line)
    city1, city2, distance = splitstrip(stripped)
    return {
        (city1, city2): int(distance),
        (city2, city1): int(distance),
    }


def build_routes(lines: list[str]) -> dict:
    return reduce(lambda a, l: a | to_dict(l), lines, {})


# Distances:


def get_distance(scores: dict, path: tuple[str, ...]) -> int:
    procs = (
        partial(sliding_window, 2),
        cmap(scores.get),
        sum,
    )
    return pipe(path, *procs)


def get_distances(data: dict) -> list[int]:
    procs = (
        dict.keys,
        chain.from_iterable,
        set,
        permutations,
        list,
        cmap(partial(get_distance, data)),
        sorted,
    )
    return pipe(data, *procs)


# Entry points:


def preprocess(data):
    procs = [
        splitstriplines,
        build_routes,
    ]
    result = pipe(data, *procs)
    return result


def part_one(data):
    routes = get_distances(data)
    return routes[0]


def part_two(data):
    routes = get_distances(data)
    return routes[-1]
