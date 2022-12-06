import pdb
import subprocess
from collections import Counter
from functools import partial, reduce, wraps
from itertools import count, groupby, product
from math import prod
from operator import itemgetter
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
    Optional,
    Sequence,
    Tuple,
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
    valmap,
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


def adjacent_transforms(
    dimensions: int, omit_origin: bool = True
) -> List[Tuple]:
    adj = product([-1, 0, 1], repeat=dimensions)
    not_origin = lambda x: not all([_ == 0 for _ in x])
    return lfilter(not_origin, adj) if omit_origin else adj


def process_input(text):
    return lcompact(text.split("\n\n"))


def load_input(fname):
    raw = Path(fname).read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    return raw


def parse_tiles(tiles):
    tiled = {}
    to_bin = {".": "0", "#": "1"}
    for tile in tiles:
        lines = splitstriplines(tile)
        ident = lines[0].removesuffix(":").split()[1]

        top = int("".join([to_bin[x] for x in lines[1]]), 2)
        bottom = int("".join([to_bin[x] for x in lines[-1]]), 2)
        cols = list(zip(*lines[1:]))
        left = int("".join([to_bin[x] for x in cols[0]]), 2)
        right = int("".join([to_bin[x] for x in cols[-1]]), 2)

        tiled[ident] = [top, right, bottom, left]
    return tiled


def invert_10bit(num):
    return int("".join(bin(num).removeprefix("0b").zfill(10)[::-1]), 2)


def invert_individual_tile(tile, orientation=None):
    assert orientation in ["vertical", "horizontal"]
    top, right, bottom, left = tile

    if orientation == "vertical":
        return [bottom, invert_10bit(right), top, invert_10bit(left)]
    else:
        return [invert_10bit(top), left, invert_10bit(bottom), right]


def invert_horizontal(tiles):
    inv = partial(invert_individual_tile, orientation="horizontal")
    return valmap(inv, tiles)


def invert_vertical(tiles):
    inv = partial(invert_individual_tile, orientation="vertical")
    return valmap(inv, tiles)


def process(data):
    pdb.set_trace()
    return


def cli_main():
    data = compose_left(load_input, process_input)("input-20.txt")
    tiles = parse_tiles(data)
    inverted_horiz = invert_horizontal(tiles)
    inverted_vert = invert_vertical(tiles)
    cc = Counter(
        list(
            concat(
                list(tiles.values())
                + list(inverted_horiz.values())
                + list(inverted_vert.values())
            )
        )
    )
    pdb.set_trace()
    answer = process(data)
    pdb.set_trace()
    print("Answer one:", answer)


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer
    cli_main()
