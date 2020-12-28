from __future__ import annotations
from dataclasses import dataclass
from functools import reduce
from typing import Any, Callable, Dict, List, Tuple
from toolz import compose_left  # type: ignore
from tutils import splitstriplines, load_and_process_input, run_tests

DAY = "12"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 25
TA2 = 286
ANSWER1 = 796
ANSWER2 = 39446


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, other: int) -> Point:
        return Point(x=self.x * other, y=self.y * other)

    def qct(self, qcts: int) -> Point:
        # quarter-circle turn, deosil positive, widdershins negative.
        procs = [lambda p: Point(p.y, -p.x)] * (qcts % 4)
        return compose_left(*procs)(Point(self.x, self.y))

    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y)


north = lambda p, amount: Point(p.x, p.y + amount)
south = lambda p, amount: Point(p.x, p.y - amount)
west = lambda p, amount: Point(p.x - amount, p.y)
east = lambda p, amount: Point(p.x + amount, p.y)
rotateleft = lambda p, amount: p.qct(-(amount // 90))
rotateright = lambda p, amount: p.qct(amount // 90)


def facing_to_direction(facing: int) -> Callable:
    dirs = {
        0: north,
        90: east,
        180: south,
        270: west,
    }
    return dirs[facing]


def forward(point: Point, facing: int, amount: int) -> Tuple[Point, int]:
    return facing_to_direction(facing)(point, amount), facing


def forward2(
    point: Point, waypoint: Point, amount: int
) -> Tuple[Point, Point]:
    return (point + (waypoint * amount)), waypoint


def left(_: Point, facing: int, amount: int) -> int:
    return (facing - amount) % 360


def right(_: Point, facing: int, amount: int) -> int:
    return (facing + amount) % 360


def handle_point(func: Callable) -> Callable:
    def inner(point: Point, facing: int, amount: int) -> Tuple:
        return func(point, amount), facing

    return inner


def handle_facing(func: Callable) -> Callable:
    def inner(point: Point, facing: int, amount: int) -> Tuple:
        return point, func(point, facing, amount)

    return inner


def handle_waypoint(func: Callable) -> Callable:
    def inner(point: Point, waypoint: Point, amount: int) -> Tuple:
        return point, func(waypoint, amount)

    return inner


def process_one(lines: List[str]) -> Any:
    point, facing = Point(x=0, y=0), 90
    moves: Dict[str, Callable] = {
        "N": handle_point(north),
        "S": handle_point(south),
        "E": handle_point(east),
        "W": handle_point(west),
        "L": handle_facing(left),
        "R": handle_facing(right),
        "F": forward,
    }

    interpreter = lambda p_f, i: moves[i[0]](*p_f, int(i[1:]))
    final_point, _ = reduce(interpreter, lines, (point, facing))
    return final_point.manhattan_distance()


def process_two(lines: List[str]) -> Any:
    point, waypoint = Point(x=0, y=0), Point(x=10, y=1)
    moves: Dict[str, Callable] = {
        "N": handle_waypoint(north),
        "S": handle_waypoint(south),
        "E": handle_waypoint(east),
        "W": handle_waypoint(west),
        "L": handle_waypoint(rotateleft),
        "R": handle_waypoint(rotateright),
        "F": forward2,
    }
    interpreter = lambda p_w, i: moves[i[0]](*p_w, int(i[1:]))
    final_point, _ = reduce(interpreter, lines, (point, waypoint))
    return final_point.manhattan_distance()


def cli_main() -> None:
    input_funcs = [splitstriplines]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process_two(data)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
