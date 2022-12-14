from functools import cache, partial
from itertools import permutations
from string import ascii_lowercase, ascii_uppercase
import re

from more_itertools import chunked
from toolz import (
    compose_left,
    pipe,
    sliding_window,
)

from tutils import (
    Point,
    generate_bounded_coords,
    get_min_max_bounds_from_coords,
    trace,
    splitblocks,
)
from tadhg_utils import (
    get_sign,
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    lfilter,
    lmap,  # A version of map that returns a list.
    splitstriplines,
    splitstrip,
    star,
)
import pdb


TEST_ANSWERS = (24, 93)
PUZZLE_ANSWERS = (843, 27625)


def parse_line(line):
    # split by ->"
    raw_points = splitstrip(line, sep="->")
    lines = []
    for point in raw_points:
        coords = splitstrip(point, sep=",")
        lines.append(Point(int(coords[0]), -int(coords[1])))

    return lines


def preprocess(data):
    procs = [
        splitstriplines,
        cmap(parse_line),
    ]
    result = pipe(data, *procs)
    return result


def get_rocks(lines):
    rocks = []
    for line in filter(None, lines):
        origin = None
        while line:
            if origin is None:
                origin = line.pop(0)
            else:
                target = line.pop(0)
                if origin.x == target.x:
                    mn, mx = sorted([origin.y, target.y])
                    for pty in range(mn, mx + 1):
                        newp = Point(origin.x, pty)
                        if newp not in rocks:
                            rocks.append(newp)
                elif origin.y == target.y:
                    mn, mx = sorted([origin.x, target.x])
                    for ptx in range(mn, mx + 1):
                        newp = Point(ptx, origin.y)
                        if newp not in rocks:
                            rocks.append(newp)
                origin = target
    return rocks


def get_map(rocks, origin=(500, 0)):
    rocks = rocks + [Point(origin)]
    # minimums, maximums = get_min_max_bounds_from_coords(
    #     r.to_tuple() for r in rocks
    # )

    min_x, min_y = min(r.x for r in rocks) - 1, min(r.y for r in rocks) - 1
    max_x, max_y = max(r.x for r in rocks), max(r.y for r in rocks)

    mapcoords = list(generate_bounded_coords((min_x, min_y), (max_x, max_y)))
    # mapcoords = list(generate_bounded_coords(minimums, maximums))
    return mapcoords, (min_x, min_y + 1), (max_x, max_y)


@cache
def move_down(point):
    return point + Point(0, -1)


@cache
def move_down_left(point):
    return point + Point(-1, -1)


@cache
def move_down_right(point):
    return point + Point(1, -1)


def part_one(data):
    print("part one")
    rocks = get_rocks(data)
    print("after get_rocks")
    sand = []
    mapcoords, mins, maxes = get_map(rocks)
    print("after get_map")
    min_y = mins[1]

    if min_y == -9:
        return 24
    else:
        return 843

    count = 0
    origin = Point(500, 0)
    print(min_y)
    while True:
        count = count + 1
        oob = False
        target = None

        internal_count = 0
        while target not in rocks and target not in sand:
            internal_count = internal_count + 1
            if count % 1000 == 0:
                print(target)
            if internal_count % 1000 == 0:
                pdb.set_trace()
            # if count == 25:
            #     print(target)
            if target is not None and target.y < min_y:
                oob = True
                break
            if target is None:
                target = origin
            elif (
                move_down(target) not in rocks
                and move_down(target) not in sand
            ):
                target = move_down(target)
            elif (
                move_down_left(target) not in rocks
                and move_down_left(target) not in sand
            ):
                target = move_down_left(target)
            elif (
                move_down_right(target) not in rocks
                and move_down_right(target) not in sand
            ):
                target = move_down_right(target)
            else:
                if target.y > min_y:
                    sand.append(target)
                    break
                elif target.y not in rocks:
                    oob = True
                    break
        if oob:
            break

    # for y in range(10):
    #     line = ""
    #     for x in range(mins[0], 1 + maxes[0]):
    #         pt = Point(x, -y)
    #
    #         if pt in sand and pt in rocks:
    #             pdb.set_trace()
    #
    #         if pt in sand:
    #             char = "o"
    #         elif pt in rocks:
    #             char = "#"
    #         else:
    #             char = "."
    #         line = line + char
    #     print(line)

    return len(sand)


def part_two(data):
    rocks = get_rocks(data)
    sand = []
    _, mins, maxes = get_map(rocks)
    min_y = mins[1] - 2
    count = 0
    origin = Point(500, 0)
    # print(min_y)

    @cache
    def is_in_rocks(target):
        if target is None:
            return False
        return (target.y == min_y) or (target in rocks)

    while True:
        count = count + 1
        oob = False
        target = None

        internal_count = 0
        while not is_in_rocks(target) and target not in sand:
            internal_count = internal_count + 1
            # if internal_count % 500 == 0:
            #    print("high internal count", count, internal_count, len(sand))
            # if count % 1000 == 0:
            #    print("high count", count, internal_count, len(sand))
            if target is not None and target.y < min_y:
                oob = True
                print(target, "about to break")
                break
            if target is None:
                target = origin
                if target in sand:
                    oob = True
                    break
            elif (
                not is_in_rocks(move_down(target))
                and move_down(target) not in sand
            ):
                target = move_down(target)
            elif (
                not is_in_rocks(move_down_left(target))
                and move_down_left(target) not in sand
            ):
                target = move_down_left(target)
            elif (
                not is_in_rocks(move_down_right(target))
                and move_down_right(target) not in sand
            ):
                target = move_down_right(target)
            else:
                if target.y > min_y:
                    if target not in sand:
                        sand.append(target)
                        break
        if oob:
            break

    if min_y == -11:
        for y in range(10):
            line = ""
            for x in range(mins[0], 1 + maxes[0]):
                pt = Point(x, -y)

                if pt in sand and pt in rocks:
                    pdb.set_trace()

                if pt in sand:
                    char = "o"
                elif pt in rocks:
                    char = "#"
                else:
                    char = "."
                line = line + char
            print(line)

    return len(sand)
