from __future__ import annotations
import datetime
from dataclasses import dataclass
from functools import partial
from typing import Callable, FrozenSet, List, Set, Tuple
from tutils import (
    OInt,
    OSet,
    until_stable,
    lmap,
    splitstriplines,
    adjacent_transforms,
    load_and_process_input,
    run_tests,
)


DAY = "11"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 37
TA2 = 26
ANSWER1 = 2303
ANSWER2 = 2057


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


FZPoint = FrozenSet[Point]


def seats_and_floor(columns: List[List[int]]) -> Tuple[FZPoint, FZPoint]:
    seats, floor = [], []
    for x, column in enumerate(columns):
        for y, cell in enumerate(column):
            newpoint = Point(x=x, y=y)
            if cell == ".":
                floor.append(newpoint)
            else:
                seats.append(newpoint)

    return (frozenset(seats), frozenset(floor))


def within_limits(extremes: Tuple[Point, Point], point: Point) -> bool:
    lower_x, lower_y = extremes[0].x, extremes[0].y
    upper_x, upper_y = extremes[1].x, extremes[1].y
    return (lower_x <= point.x <= upper_x) and (lower_y <= point.y <= upper_y)


def lifecycle1(
    seats_floor: Tuple[FZPoint, FZPoint], adj: Set[Point], occ: Set[Point]
) -> Set[Point]:
    seats, floor = seats_floor
    total = frozenset(seats.union(floor))
    limitcheck = partial(within_limits, (min(total), max(total)))
    next_occupied = set()
    for seat in seats:
        visible = count_visible(occ, limitcheck, floor, seat, adj, maxring=1)
        if (seat in occ and visible < 4) or (seat not in occ and visible < 1):
            next_occupied.add(seat)
    return next_occupied


def process_one(seats: Set[Point]) -> int:
    adjacent = {Point(*a) for a in adjacent_transforms(2, omit_origin=True)}
    cycle = partial(lifecycle1, seats, adjacent)
    stable = until_stable(cycle)(set())
    return len(stable)


def count_visible(
    occ: Set[Point],
    limitcheck: Callable,
    floor: FZPoint,
    origin: Point,
    adj: OSet = None,
    ring: int = 1,
    ct: int = 0,
    maxring: OInt = None,
) -> int:
    # keep calling self utnil there are no relative points left in adj
    if (not adj) or (ct >= 5) or (maxring and ring > maxring):
        return ct
    to_remove = set()
    for drc in adj:
        neighbor = (drc * ring) + origin
        if neighbor in occ:
            ct = ct + 1
            to_remove.add(drc)
        elif (not limitcheck(neighbor)) or (neighbor not in floor):
            to_remove.add(drc)
    if len(to_remove) == len(adj):
        return ct
    adj = adj.difference(to_remove)
    return count_visible(
        occ, limitcheck, floor, origin, adj, ring + 1, ct, maxring
    )


def lifecycle2(
    seats_floor: Tuple[FZPoint, FZPoint], occ: Set[Point], dirs: Set[Point]
) -> Set[Point]:
    seats, floor = seats_floor
    total = frozenset(seats.union(floor))
    limitcheck = partial(within_limits, (min(total), max(total)))
    next_occupied = set()
    for seat in seats:
        visible = count_visible(occ, limitcheck, floor, seat, adj=dirs.copy())
        if (seat in occ and visible < 5) or (seat not in occ and visible < 1):
            next_occupied.add(seat)
    return next_occupied


def process_two(seats_floor: Tuple[Set[Point], Set[Point]]) -> int:
    adjacent = {Point(*a) for a in adjacent_transforms(2, omit_origin=True)}
    cycle = partial(lifecycle2, seats_floor, dirs=adjacent)
    stable = until_stable(cycle)(set())
    return len(stable)


def cli_main() -> None:
    input_funcs = [
        splitstriplines,
        partial(lmap, list),
        lambda lst: list(zip(*lst)),  # make it so that (x, y) is lst[x][y].
        seats_and_floor,
    ]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    pre_one = datetime.datetime.now()
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one, datetime.datetime.now() - pre_one)
    pre_two = datetime.datetime.now()
    answer_two = process_two(data)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two, datetime.datetime.now() - pre_two)


if __name__ == "__main__":
    cli_main()
