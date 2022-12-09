from functools import partial

from tutils import Point, adjacent_transforms
from tadhg_utils import (
    get_sign,  # anything below zero -> -1, 0 -> 0, anything above zero -> 1.
    lmap,  # A version of map that returns a list.
    splitstriplines,
)


TEST_ANSWERS = (13, 1)
PUZZLE_ANSWERS = (5907, 2303)
DIRECTIONS = {
    "u": Point(0, 1),
    "d": Point(0, -1),
    "l": Point(-1, 0),
    "r": Point(1, 0),
}


def parse_move(line):
    direction, amount = line.split(" ")
    return direction.lower(), int(amount)


def move_pt_one(pos: Point, direction: str):
    return pos + DIRECTIONS[direction]


def are_adjacent(head: Point, tail: Point):
    neighbors = map(lambda x: head + Point(*x), adjacent_transforms(2))
    return (head == tail) or (tail in neighbors)


def move_tail_towards_head(head: Point, tail: Point):
    diff = head - tail
    return tail + Point(get_sign(diff.x), get_sign(diff.y))


def move_rope(visited: set, rope: list[Point], move: tuple[str, int]):
    direction, amount = move
    for _ in range(amount):
        visited, rope = move_rope_knots(visited, rope, direction)

    return visited, rope


def move_rope_knots(visited: set, rope: list[Point], direction: str):
    rope = [move_pt_one(rope[0], direction)] + rope[1:]
    move = partial(move_knot, rope)
    newrope = [rope[0]] + [move(j, knot) for j, knot in enumerate(rope[1:])]
    return visited | {newrope[-1]}, newrope


def move_knot(rope: list[Point], incr: int, current: Point):
    # Since we're enumerating rope[1:], rope[incr] gets us what we want here:
    last = rope[incr]
    if are_adjacent(last, current):
        return current
    return move_tail_towards_head(last, current)


def get_visits(knots: int, moves: list[tuple[str, int]]):
    rope, visited = [Point(0, 0)] * knots, {Point(0, 0)}
    for move in moves:
        visited, rope = move_rope(visited, rope, move)
    return len(visited)


def preprocess(data):
    return lmap(parse_move, splitstriplines(data))


def part_one(data):
    return get_visits(2, data)


def part_two(data):
    return get_visits(10, data)
