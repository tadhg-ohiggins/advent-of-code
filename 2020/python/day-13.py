import pdb
import subprocess
from collections import Counter
from functools import partial, reduce, wraps
from itertools import count, groupby
from math import lcm
from operator import itemgetter, mul
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


def earliest(target, num):
    for i in range(target - num, target + num + 1):
        if i % num == 0:
            if (target - i) < target:
                nearest = i + num
            return (num, nearest, i)


def testprocess():
    testinput = ["939", "7,13,x,x,59,x,31,19"]
    return process_one(testinput)


# def gettimestamp(start, offset,


def testprocesstwo():
    testinput = ["939", "7,13,x,x,59,x,31,19"]
    return process_two(testinput)


def process_two(data, start=None, limit=None):

    blines = [int(_) if _ != "x" else _ for _ in data[1].split(",")]
    targets = [(item, i) for i, item in enumerate(blines) if item != "x"]
    lowest = lcm(*[_[0] for _ in targets])
    numbers = [_[0] for _ in targets]
    offsets = [_[1] for _ in targets]
    lcms = [x for x in targets if x[1] in numbers] + [targets[0]]
    steps = [lcm(*x) for x in lcms]
    realstepstest = [x for x in steps if (x != 0) and x % numbers[0] == 0]
    if realstepstest:
        realsteps = realstepstest[0]
        stepbase = realsteps / numbers[0]
        startoffset = [x for x in targets if x[0] == stepbase][0][1]
        reloffsets = [(x, i - startoffset) for x, i in targets]
    else:
        startoffset = 0
        stepbase = 1
        reloffsets = targets

    # pdb.set_trace()
    # startnum = 1 start if start else 1
    startnum = stepbase
    if start:
        startnum = start

    ctr = count(startnum, stepbase)
    print(stepbase)
    while True:
        i = next(ctr)
        conds = [((i + offset) % num) == 0 for num, offset in reloffsets]
        # print(conds)
        if all([((i + offset) % num) == 0 for num, offset in reloffsets]):
            return i - startoffset
        if limit:
            if i > limit:
                assert False


def p3(data):
    blines = [int(_) if _ != "x" else _ for _ in data[1].split(",")]
    targets = [(item, i) for i, item in enumerate(blines) if item != "x"]
    # lowest = lcm(*[_[0] for _ in targets])
    numbers = [_[0] for _ in targets]
    offsets = [_[1] for _ in targets]
    # total = reduce(mul, numbers, 1)
    subtract = chinese_remainder(numbers, offsets)
    mult = reduce(mul, numbers)
    # print(mult)
    # print(subtract)
    return mult - subtract
    """
    The above circuitous approach just happened to work; I had the remainders
    inverted here (if 13 departs one minute after 7, its remainder is -1, or
    12, not 1). With the above, if you multiply them all together and then
    subtract the chinese remainder theorem result with the reversed remainders,
    you get the same as if you just ran the theorem on the correct
    remainders.
    """
    running = 1
    # return total - subtract

    for target, offset in targets:
        running = (target - offset) * running
        print(running)
    return running  # - subtract


def process_one(data):
    target = int(data[0])
    nums = [int(_) for _ in data[1].split(",") if _ != "x"]
    bst = sorted([earliest(target, num) for num in nums], key=itemgetter(1))[0]
    return bst[0] * (bst[1] - target)


def chinese_remainder(n, a):

    total = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        total += a_i * mul_inv(p, n_i) * p
    return total % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def process(text):
    lines = lcompact(text.splitlines())
    testanswer = testprocess()
    assert testanswer == 295
    answer_one = process_one(lines)
    testanswertwo = testprocesstwo()
    examples = [
        # (["939", "7,13"], 1068781),
        (["939", "7,13,59"], 77),
        # (["939", "7,13,x,x,59,x,31,19"], 1068781),
        # (["939", "7,13,x,x,59,x,31,19"], 1068781),
        # (["", "17,x,13,19"], 3417),
        # (["", "67,x,7,59,61"], 779210),
        # (["", "67,7,x,59,61"], 1261476),
        # (["", "1789,37,47,1889"], 1202161486),
    ]
    for data, expected in []:
        print(data)
        if expected != 1202161486:
            # answer = process_two(data, limit=expected)
            answer = p3(data)

        else:
            answer = process_two(data, start=1202000000, limit=expected)
        print(answer)
        # assert answer == expected

    # a2 = process_two(lines)
    # a2 = process_two(lines, start=99999999986266)
    a3 = p3(examples[0][0])
    a2 = process_two(examples[0][0])
    a4 = p3(lines)

    pdb.set_trace()
    return


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer

    raw = Path("input-13.txt").read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    result = process(raw)
