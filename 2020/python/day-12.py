import math
import pdb
import subprocess
from collections import Counter
from functools import partial, reduce, wraps
from itertools import groupby
from operator import itemgetter
from pathlib import Path
from pprint import pprint
from string import (
    ascii_lowercase,
    digits as ascii_digits,
)
from typing import Any, Callable, List, Iterable, Optional, Sequence, Union
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
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lpluck = compose_left(pluck, list)  # lambda k, l: [*pluck(f, l)]
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
lcompact = partial(lfilter, None)
splitstrip = compose_left(str.split, partial(lmap, str.strip), lcompact)
make_incr = lambda: partial(next, iterate(lambda x: x + 1, 0))


def lnoncontinuous(array: list[int]):
    return lmap(list, noncontinuous(array))


def north(point, amount):
    x, y = point
    return x, y + amount


def south(point, amount):
    x, y = point
    return x, y - amount


def west(point, amount):
    x, y = point
    return x - amount, y


def east(point, amount):
    x, y = point
    return x + amount, y


def rotate(origin, point, degrees):
    """
    Rotate a point clockwise by a given angle around a given origin.

    """
    degrees = degrees * -1
    angle = math.radians(degrees)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return round(qx), round(qy)


def rotaterelleft(origin, relpoint, degrees):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    """
    degrees = degrees * -1
    newpoint = rotate(origin, point_add(origin, relpoint), degrees)
    newrelpoint = point_sub(newpoint, origin)
    return origin, newrelpoint


def rotaterelright(origin, relpoint, degrees):
    """
    Rotate a point clockwise by a given angle around a given origin.

    """
    newpoint = rotate(origin, point_add(origin, relpoint), degrees)
    newrelpoint = point_sub(newpoint, origin)
    return origin, newrelpoint


def facing_to_direction(facing):
    dirs = {
        0: north,
        90: east,
        180: south,
        270: west,
    }
    if facing not in dirs:
        pdb.set_trace()
    return dirs[facing]


def forward(facing, point, amount):
    return facing_to_direction(facing)(point, amount)


def point_add(point, rel):
    ox, oy = point
    rx, ry = rel
    return (ox + rx, oy + ry)


def point_sub(origin, point):
    ox, oy = origin
    rx, ry = point
    return (ox - rx, oy - ry)


def forward2(point, relativewaypoint, amount):
    for _ in range(amount):
        point = point_add(point, relativewaypoint)
    return point, relativewaypoint


def changefacing(facing, rotation, amount):
    if rotation == "right":
        return (facing + amount) % 360
    if rotation == "left":
        return (facing - amount) % 360


def left(facing, point, amount):
    return changefacing(facing, "left", amount)


def right(facing, point, amount):
    return changefacing(facing, "right", amount)


def instr(text, point, facing):
    forwardf = partial(forward, facing)
    leftf = partial(left, facing)
    rightf = partial(right, facing)
    moves = {
        "N": [north],
        "S": [south],
        "E": [east],
        "W": [west],
        "L": [leftf],
        "R": [rightf],
        "F": [forwardf],
    }
    move = text[0]
    amount = int(text[1:])
    if move in "LR":
        facing = moves[move][0](point, amount)
    else:
        point = moves[move][0](point, amount)

    return point, facing


def instr2(text, point, waypoint):
    leftf = rotaterelleft
    rightf = rotaterelright
    moves = {
        "N": [north],
        "S": [south],
        "E": [east],
        "W": [west],
        "L": [leftf],
        "R": [rightf],
        "F": [forward2],
    }
    move = text[0]
    amount = int(text[1:])
    if move in "LRF":
        point, waypoint = moves[move][0](point, waypoint, amount)
    else:
        # pdb.set_trace()
        waypoint = moves[move][0](point_add(point, waypoint), amount)
        waypoint = point_sub(waypoint, point)

    return point, waypoint


def process(text):
    lines = lcompact(text.strip().splitlines())
    # lines = ["F10", "N3", "F7", "R90", "F11"]
    """
    point = (0, 0)
    facing = 90

    for i, line in enumerate(lines):
        if i < 20:
            print(point, facing, line)
        point, facing = instr(line, point, facing)
        if i < 20:
            print("processed", point, facing)

    mdist = sum(lmap(abs, point))
    """
    point = (0, 0)
    waypoint = (10, 1)
    for i, line in enumerate(lines):
        if i < 20:
            print(point, waypoint, line)
        point, waypoint = instr2(line, point, waypoint)
        if i < 20:
            print("processed", point, waypoint)

    mdist = sum(lmap(abs, point))
    pdb.set_trace()
    return


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer

    raw = Path("input-12.txt").read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    result = process(raw)
