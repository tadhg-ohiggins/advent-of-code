import pdb
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass, fields
from functools import partial, reduce, wraps
from itertools import count, groupby
from math import prod
from more_itertools import split_at
from operator import attrgetter, itemgetter
from pathlib import Path
from pprint import pprint
from string import (
    ascii_lowercase,
    digits as ascii_digits,
)
from typing import (
    Any,
    Callable,
    List,
    Iterable,
    NamedTuple,
    Optional,
    Sequence,
    Union,
)
from toolz import (  # type: ignore
    compose_left,
    concat,
    curry,
    do,
    excepts,
    iterate,
    keyfilter,
    pluck,
    pipe,
    sliding_window,
)


IterableS = Iterable[str]
hexc = ["a", "b", "c", "d", "e", "f"] + list(ascii_digits)


def toolz_pick(keep: IterableS, d: dict) -> dict:
    return keyfilter(lambda x: x in keep, d)


def toolz_omit(remove: IterableS, d: dict) -> dict:
    return keyfilter(lambda x: x not in remove, d)


def pick(keep: IterableS, d: dict) -> dict:
    return {k: d[k] for k in d if k in keep}


def omit(remove: IterableS, d: dict) -> dict:
    return {k: d[k] for k in d if k not in remove}


def add_debug(debug_f: Callable, orig_f: Callable) -> Callable:
    """
    Transforms the function such that output is passed
    to the debug function before being returned as normal.

    add_debug(print, str.upper) would return a function equivalent to:

    def fn(val: str): -> str
        result = str.upper(val)
        print(result)
        return result
    """
    do_f = partial(do, debug_f)
    return compose_left(orig_f, do_f)


def add_debug_list(debug_f: Callable, funcs: List[Callable]) -> List[Callable]:
    """
    Transforms each of the functions such that the output of each is passed
    to the debug function before being returned as normal.
    """
    return [add_debug(debug_f, f) for f in funcs]


def run_process(
    command: Union[list, str], options: Optional[dict] = None
) -> subprocess.CompletedProcess:
    base_opts = {"check": True, "text": True, "capture_output": True}
    opts = options if options else {}
    # pylint: disable=subprocess-run-check
    # return subprocess.run(command, **{**base_opts, **opts})  # type: ignore
    return subprocess.run(command, **(base_opts | opts))  # type: ignore


def until_stable(func: Callable) -> Callable:
    """
    Repeatedly call the same function on its arguments until the result doesn't
    change.

    Not sure how to make this work in variadic cases; comparing a single result
    to *args doesn't seem to work.
    """

    def inner(arg: Any, **kwds: Any) -> Any:
        if func(arg, **kwds) == arg:
            return arg
        return inner(func(arg, **kwds))

    return inner


def oxford(lst: List[str]) -> str:
    """
    Turns a list into a properly-formatted list phrase.
    ``["something"]`` becomes "something".
    ``["thing1", "thing2"]`` becomes "thing1 and thing2".
    ``["thing1", "thing2", "thing3"]`` becomes "thing1, thing2, and thing3".
    ``["a", "b", "c", "d"]`` becomes "a, b, c, and d".
    """
    if len(lst) <= 2:
        return " and ".join(lst)
    return f'{", ".join(lst[:-1])}, and {lst[-1]}'


def excepts_wrap(err: Any, err_func: Callable) -> Callable:
    """
    This basically means that::

        @excepts_wrap(ValueError, lambda _: None)
        def get_formatted_time(fmt: str, value: str) -> Optional[datetime]:
            return datetime.strptime(value.strip(), fmt)

        gft = get_formatted_time

    With the decorator, that's broadly equivalent to this without
    any decorator::

        gft = excepts(
            ValueError,
            get_formatted_time,
            lambda _: None
        )

    """

    def inner_excepts_wrap(fn: Callable) -> Callable:
        return excepts(err, fn, err_func)

    return inner_excepts_wrap


def firstwhere(pred: Callable, seq: Sequence) -> Any:
    return next(filter(pred, seq), False)


def noncontinuous(array: list[int]):
    """
    noncontinuous([1, 2, 3, 5, 6, 8, 9, 10]) == [[1, 2, 3], [5, 6], [8, 9, 10]]

    The difference between a number and its index will be stable for a
    consecutive run, so we can group by that.

    -1 for 1, 2, and 3; -2 for 5 and 6; -3 for 8, 9 and 10 in the above list.

    enumerate gets us item and index, a quick x[0] - x[1] lambda gets us the
    difference.

    Once we have them in groups, we extract them into the lists of runs.

    This could be all iterators instead of lists, but I'll make another
    function to do that translation.

    See also consecutive_groups in more_itertools, which was the basis for
    this.
    """
    check = lambda x: x[0] - x[1]
    collate = lambda x: map(itemgetter(1), list(x)[1])
    return map(collate, groupby(enumerate(array), key=check))


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lcompact = partial(lfilter, None)
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lpluck = compose_left(pluck, list)  # lambda k, l: [*pluck(f, l)]
lstrip = partial(lmap, str.strip)
splitstrip = compose_left(str.split, lstrip, lcompact)
splitstriplines = compose_left(str.splitlines, lstrip, lcompact)
seq_to_dict = compose_left(lmap, dict)
split_to_dict = lambda s, **kwds: seq_to_dict(partial(splitstrip, **kwds), s)
c_map = curry(map)
c_lmap = curry(lmap)
is_char_az = partial(lambda y, x: x in y, ascii_lowercase)
is_char_hex = partial(lambda y, x: x in y, hexc)
is_char_az09 = partial(lambda y, x: x in y, ascii_lowercase + ascii_digits)
filter_str = partial(lambda f, s: "".join(filter(f, s)))
filter_az = partial(filter_str, is_char_az)
filter_az09 = partial(filter_str, is_char_az09)
filter_hex = partial(filter_str, is_char_hex)
add_pprint = partial(add_debug, pprint)
add_pprinting = partial(lmap, add_pprint)
make_incrementer = lambda start=0, step=1: partial(next, count(start, step))


def lnoncontinuous(array: list[int]):
    return lmap(list, noncontinuous(array))


def process_input(text):
    return lcompact(text.splitlines())


def load_input(fname):
    raw = Path(fname).read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    return raw


@dataclass
class Point:
    on: bool
    x: int
    y: int
    z: int


@dataclass
class PointMin:
    x: int
    y: int
    z: int


@dataclass
class Point4:
    on: bool
    x: int
    y: int
    z: int
    w: int


@dataclass
class Point4Min:
    x: int
    y: int
    z: int
    w: int


def pt_to_ptmin(point: Point) -> PointMin:
    fnames = {
        f.name: getattr(point, f.name) for f in fields(point) if f.name != "on"
    }
    return PointMin(**fnames)


def pt_to_pt4min(point: Point) -> PointMin:
    fnames = {
        f.name: getattr(point, f.name) for f in fields(point) if f.name != "on"
    }
    return Point4Min(**fnames)


def pt_to_pt4(point: Point) -> Point4:
    return Point4(on=point.on, x=point.x, y=point.y, z=point.z, w=0)


def lines_to_points(lines: List[str]) -> Point:
    # middle one is always z zero.
    sections = [lines]
    points = []
    xplanes = []
    for i, z in enumerate(sections):
        print(i, z)
        xlines = []
        lines = z
        for j, y in enumerate(lines):
            xpoints = []
            for k, x in enumerate(y):
                points.append(Point(False, k, j, i))
                xpoints.append(x)
            xlines.append(xpoints)
        xplanes.append(xlines)

    for point in points:
        x, y, z = point.x, point.y, point.z
        value = xplanes[z][y][x]
        print(value)
        point.on = value == "#"

    return points, xplanes


def count_coord_values(points, coord) -> int:
    return len(set(map(attrgetter(coord), points)))


def points_to_grids(points: List[Point]) -> List[List[List[str]]]:
    zs, ys, xs = [count_coord_values(points, c) for c in ("z", "y", "x")]
    ctr = make_incrementer()
    grid = [[[[""] for _ in range(xs)] for _ in range(ys)] for _ in range(zs)]
    for point in points:
        value = "#" if point.on else "."
        x, y, z = point.x, point.y, point.z
        grid[z][y][x] = value

    return grid


def points4_to_grids(points: List[Point]) -> List[List[List[str]]]:
    zs, ys, xs, ws = [
        count_coord_values(points, c) for c in ("z", "y", "x", "w")
    ]
    grid = [
        [[[[""] for _ in range(xs)] for _ in range(ys)] for _ in range(zs)]
        for _ in range(ws)
    ]
    for point in points:
        value = "#" if point.on else "."
        x, y, z, w = point.x, point.y, point.z, pointw
        grid[z][y][x][w] = value

    return grid


def coord_fnames(point):
    return [f.name for f in fields(point) if f.name != "on"]


def xfind_adjacent(points, point):
    adj = [
        p
        for p in points
        if all(
            [
                abs(p.x - point.x) <= 1,
                abs(p.y - point.y) <= 1,
                abs(p.z - point.z) <= 1,
                not (p.z == point.z and p.y == point.y and p.x == point.x),
            ]
        )
    ]
    return adj


def find_adjacent(points, point):
    fnames = coord_fnames(point)

    adj = [
        p
        for p in points
        if all(
            [
                abs(getattr(p, field) - getattr(point, field)) <= 1
                for field in fnames
            ]
        )
        and not all(
            [getattr(p, field) == getattr(point, field) for field in fnames]
        )
    ]
    return adj


def count_active(points):
    return len(lfilter(lambda p: p.on, points))


def count_active_neighbors(points, point):
    return count_active(find_adjacent(points, point))


def count_inactive_neighbors(points, point):
    return len(lfilter(lambda p: not p.on, find_adjacent(points, point)))


def pt_to_str(point):
    # return f"{point.x}.{point.y}.{point.z}"
    return ".".join([str(getattr(point, f)) for f in coord_fnames(point)])


def add_adjacent(points):
    pointsmin = [pt_to_ptmin(pt) for pt in points]
    # print(len(pointsmin))
    spoints = [pt_to_str(p) for p in points]
    # print(len(spoints))
    # print(len(set(spoints)))
    added = []
    for point in pointsmin:
        for x in range(point.x - 1, point.x + 2):
            for y in range(point.y - 1, point.y + 2):
                for z in range(point.z - 1, point.z + 2):
                    pmin = PointMin(x, y, z)
                    spmin = pt_to_str(pmin)
                    if spmin not in spoints and spmin not in added:
                        added.append(spmin)
                        points.append(Point(on=False, x=x, y=y, z=z))
    spoints = [pt_to_str(p) for p in points]
    # print(len(spoints))
    # print(len(set(spoints)))
    # pdb.set_trace()
    return points


def add_adjacent4(points):
    try:
        pointsmin = [pt_to_pt4min(pt) for pt in points]
    except:
        pdb.set_trace()
    # print(len(pointsmin))
    spoints = [pt_to_str(p) for p in points]
    # print(len(spoints))
    # print(len(set(spoints)))
    added = []
    for point in pointsmin:
        for x in range(point.x - 1, point.x + 2):
            for y in range(point.y - 1, point.y + 2):
                for z in range(point.z - 1, point.z + 2):
                    for w in range(point.w - 1, point.w + 2):
                        pmin = Point4Min(x, y, z, w)
                        spmin = pt_to_str(pmin)
                        if spmin not in spoints and spmin not in added:
                            added.append(spmin)
                            points.append(Point4(on=False, x=x, y=y, z=z, w=w))
    spoints = [pt_to_str(p) for p in points]
    # print(len(spoints))
    # print(len(set(spoints)))
    # pdb.set_trace()
    return points


def cycle_step(points, func, klass):
    expanded = func(points)
    newpoints = []
    # print(len(expanded))
    for point in expanded:
        newpoint, on = None, None
        if point.on:
            on = count_active_neighbors(points, point) in (2, 3)
        else:
            on = count_active_neighbors(points, point) == 3
        newpointd = asdict(point) | {"on": on}
        # newpoint = Point(on=on, x=point.x, y=point.y, z=point.z)
        newpoint = klass(**newpointd)
        newpoints.append(newpoint)

    return newpoints


def process(data):
    points, planes = lines_to_points(data)
    print("active at start:", count_active(points))
    # arrays = points_to_grids(points)
    # assert arrays == planes
    # points = cycle_step(points)
    # pprint(arrays)
    """
    newpoints = points[:]
    for i in range(6):
        print(i, count_active(newpoints))
        newpoints = cycle_step(newpoints, add_adjacent, Point)
    print("Answer after", i + 1, count_active(newpoints))

    """
    wpoints = [pt_to_pt4(p) for p in points]
    for i in range(6):
        print(i, count_active(wpoints))
        wpoints = cycle_step(wpoints, add_adjacent4, Point4)
    print("Answer after", i + 1, count_active(wpoints))

    pdb.set_trace()
    return


testdata = [
    ".#.",
    "..#",
    "###",
]


testdata_answer_cycles = [
    "\n".join(
        [
            "z=-1",
            "#..",
            "..#",
            ".#.",
            "",
            "z=0",
            "#.#",
            ".##",
            ".#.",
            "",
            "z=1",
            "#..",
            "..#",
            ".#.",
        ]
    )
]


def cli_main():
    data = compose_left(load_input, process_input)("input-17.txt")
    answer = process(testdata)
    assert answer == 112
    # pdb.set_trace()
    # answer = process(data)
    # pdb.set_trace()
    print("Answer one:", answer)


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer
    cli_main()
