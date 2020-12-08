import pdb
import subprocess
from functools import partial, reduce, wraps
from math import prod
from pathlib import Path
from pprint import pprint
from string import (
    ascii_lowercase,
    digits as ascii_digits,
)
from typing import Any, Callable, List, Iterable, Optional, Union
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


def proc_line(lines, current, acc, seen):
    seen = seen + [current]
    cmd, amt = splitstrip(lines[current], " ")
    if cmd in ("nop", "acc"):
        nxt = current + 1
    if cmd == "jmp":
        nxt = current + int(amt)
    if cmd == "acc":
        acc = acc + int(amt)
    if nxt in seen:
        return acc
    else:
        return proc_line(lines, nxt, acc, seen)


def proc_line2(lines, current, acc, seen, changed):
    print(current)
    try:
        print(lines[current])
    except:
        return acc

    seen = seen + [current]
    cmd, amt = splitstrip(lines[current], " ")
    if cmd in ("nop", "acc"):
        nxt = current + 1
    if cmd == "jmp":
        nxt = current + int(amt)
    if cmd == "acc":
        acc = acc + int(amt)
    if nxt in seen:
        print("seen", lines[current], nxt)
        return False
    else:
        return proc_line2(lines, nxt, acc, seen, changed)


def process(text):
    origlines = lcompact(text.splitlines())
    lines = origlines[:]
    # acc = proc_line(lines, 0, 0, [])
    # acc = proc_line2(lines, 0, 0, [], False)
    # newlines = lines[:]
    # newlines[195] = newlines[195].replace("nop", "jmp")
    make_counter = lambda: partial(next, iterate(lambda x: x + 1, 0))
    ctr = make_counter()
    while True:
        seen = []
        acc = proc_line2(lines, 0, 0, seen, False)
        if acc != False:
            print("yo", acc)
            break
        i = ctr()
        lines = origlines[:]
        if "jmp" in lines[i]:
            lines[i] = lines[i].replace("jmp", "nop")
        elif "nop" in lines[i]:
            lines[i] = lines[i].replace("nop", "jmp")
        print(lines)
        seen = []
        acc = proc_line2(lines, 0, 0, seen, False)
        print("acc", acc)
        if acc != False:
            print("yo", acc)
            break
        # print(lines[i])

    pdb.set_trace()
    return


test_lines = [
    "nop +0",
    "acc +1",
    "jmp +4",
    "acc +3",
    "jmp -3",
    "acc -99",
    "acc +1",
    "jmp -4",
    "acc +6",
]


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer

    raw = Path("input-08.txt").read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    result = process(raw)
