from functools import partial, reduce
from itertools import takewhile
from operator import mul

from tadhg_utils import (
    lmap,  # A version of map that returns a list.
    splitstriplines,
)


TEST_ANSWERS = (21, 8)
PUZZLE_ANSWERS = (1705, 371200)


def mirror_split(seq: list | str, pos: int) -> list:
    # mirror_split(["abcdef", 2) -> ["ba", "def"]
    return [seq[:pos][::-1], seq[pos + 1 :]]


def vis_clear(height: int, seq: list[int]) -> bool:
    return all(t < height for t in seq)


def eval_tree(data: list, linenum: int, colnum: int) -> bool:
    if linenum in (0, len(data[0]) - 1) or colnum in (0, len(data) - 1):
        return True

    line = lmap(int, data[linenum])
    height = line[colnum]
    clear = partial(vis_clear, height)

    if clear(line[:colnum]) or clear(line[colnum + 1 :]):
        return True

    col = lmap(int, [data[ln][colnum] for ln in range(len(data))])
    return clear(col[:linenum]) or clear(col[linenum + 1 :])


def get_score_for_trees(height: int, trees: list[int]) -> int:
    result = len(list(takewhile(lambda x: x < height, trees)))
    # Account for the difference between reaching the edge versus hitting a
    # tree:
    return result if len(trees) == result else result + 1


def eval_visible_distance(data: list[str], linenum: int, colnum: int) -> int:
    if linenum in (0, len(data[0]) - 1) or colnum in (0, len(data) - 1):
        return 0

    line = lmap(int, data[linenum])
    col = lmap(int, [data[ln][colnum] for ln in range(len(data))])
    height = line[colnum]

    directions = mirror_split(line, colnum) + mirror_split(col, linenum)
    vis_scores = map(partial(get_score_for_trees, height), directions)

    return reduce(lambda acc, v: mul(acc, v), vis_scores, 1)


preprocess = splitstriplines


def part_one(data: list[str]):
    return sum(
        eval_tree(data, i, j)
        for i, _ in enumerate(data)
        for j in range(len(data[i]))
    )


def part_two(data: list[str]):
    def reducer(acc, v):
        return max(acc, eval_visible_distance(data, v[0], v[1]))

    coords = ((i, j) for i, _ in enumerate(data) for j in range(len(data[i])))
    return reduce(reducer, coords, 0)
