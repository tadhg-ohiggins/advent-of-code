from toolz import pipe

from tutils import Point, adjacent_transforms
from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    lmap,  # A version of map that returns a list.
    splitstriplines,
)


TEST_ANSWERS = (13, 1)
PUZZLE_ANSWERS = (5907, 2303)


def parse_move(line):
    direction, amount = line.split(" ")
    return direction.lower(), int(amount)


def move_pt_one(pos: Point, direction: str):
    if direction == "u":
        return pos + Point(0, 1)
    if direction == "d":
        return pos - Point(0, 1)
    if direction == "l":
        return pos - Point(1, 0)
    if direction == "r":
        return pos + Point(1, 0)
    return None


def are_adjacent(head: Point, tail: Point):
    neighbors = lmap(lambda x: head + Point(*x), adjacent_transforms(2))
    return (head == tail) or (tail in neighbors)


def abs_lim_1(value: int):
    if value < 0:
        return max([-1, value])
    return min([1, value])


def move_tail_towards_head(head: Point, tail: Point):
    if head.x == tail.x:
        if head.y > tail.y:
            tail = tail + Point(0, 1)
        else:
            tail = tail - Point(0, 1)
    elif head.y == tail.y:
        if head.x > tail.x:
            tail = tail + Point(1, 0)
        else:
            tail = tail - Point(1, 0)
    else:
        diff = Point(*map(abs_lim_1, list(head - tail)))
        tail = tail + diff
    return tail


def move_head_and_tail(
    visited: set, head: Point, tail: Point, move: tuple[str, int]
):
    direction, amount = move
    for _ in range(amount):
        head = move_pt_one(head, direction)
        if not are_adjacent(head, tail):
            tail = move_tail_towards_head(head, tail)
            visited = visited | {tail}
    return visited, head, tail


def move_rope(visited: set, rope: list[Point], move: tuple[str, int]):
    direction, amount = move
    for _ in range(amount):
        visited, rope = move_rope_knots(visited, rope, direction)

    return visited, rope


def move_rope_knots(visited, rope, direction):
    newrope = []
    for j, knot in enumerate(rope):
        if j == len(rope):
            break
        if j == 0:
            newrope.append(move_pt_one(knot, direction))
            continue
        if not are_adjacent(newrope[j - 1], rope[j]):
            newrope.append(move_tail_towards_head(newrope[j - 1], rope[j]))
        else:
            newrope.append(rope[j])

    return visited | {newrope[-1]}, newrope


def preprocess(data):
    procs = [
        splitstriplines,
        cmap(parse_move),
    ]
    result = pipe(data, *procs)
    return result


def part_one(data):
    head = Point(0, 0)
    tail = Point(0, 0)
    visited = {tail}
    for move in data:
        visited, head, tail = move_head_and_tail(visited, head, tail, move)
    return len(visited)


def part_two(data):
    rope = [Point(0, 0)] * 10
    visited = {rope[-1]}
    for move in data:
        visited, rope = move_rope(visited, rope, move)

    return len(visited)
