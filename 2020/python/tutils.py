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
    juxt,
    keyfilter,
    pluck,
    pipe,
    sliding_window,
)


# pylint: disable=unsubscriptable-object
IterableS = Iterable[str]
OInt = Optional[int]
ODict = Optional[dict]
UListStr = Union[list, str]
# pylint: enable=unsubscriptable-object
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
    command: UListStr, options: ODict = None
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


def nextwhere(pred: Callable, seq: Sequence) -> Any:
    return next(filter(pred, seq), False)


def noncontinuous(array: List[int]) -> Iterable:
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


def lnoncontinuous(array: List[int]) -> List[List[int]]:
    return lmap(list, noncontinuous(array))


def adjacent_transforms(
    dimensions: int, omit_origin: bool = True
) -> List[Tuple]:
    adj = product([-1, 0, 1], repeat=dimensions)
    not_origin = lambda x: not all([_ == 0 for _ in x])
    return lfilter(not_origin, adj) if omit_origin else adj


def load_and_process_input(fname: str, input_funcs: List[Callable]) -> Any:
    processinput = partial(process_input, input_funcs)
    return compose_left(load_input, processinput)(fname)


def load_input(fname: str) -> str:
    return Path(fname).read_text().strip()


def process_input(input_funcs: List[Callable], text: str) -> Any:
    return compose_left(*input_funcs)(text)


def tests(
    testfile: str,
    tanswer_one: Any,
    tanswer_two: Any,
    answer_one: Any,
    input_funcs: List[Callable],
    process_one: Callable,
    process_two: Callable,
) -> Any:
    testdata = load_and_process_input(testfile, input_funcs)
    result = process_one(testdata)
    if result != tanswer_one:
        pdb.set_trace()
    assert result == tanswer_one
    print("Test answer one:", result)
    if answer_one is not None:
        result_two = process_two(testdata)
        if tanswer_two is not None:
            if result_two != tanswer_two:
                pdb.set_trace()
            assert result_two == tanswer_two
            print("Test answer two:", result_two)


def run_tests(
    testfile: str,
    tanswer_one: Any,
    tanswer_two: Any,
    answer_one: Any,
    input_funcs: List[Callable],
    process_one: Callable,
    process_two: Callable,
) -> None:
    if Path(testfile).exists():
        tests(
            testfile,
            tanswer_one,
            tanswer_two,
            answer_one,
            input_funcs,
            process_one,
            process_two,
        )


""" END HELPER FUNCTIONS """


DAY = "00"
INPUT = f"input-{DAY}.txt"
TEST = f"test-input-{DAY}.txt"
TESTANSWER_ONE = None
TESTANSWER_TWO = None
ANSWER_ONE = None
ANSWER_TWO = None


def process_one(data: Any) -> Any:
    pdb.set_trace()
    return


def process_two(data: Any) -> Any:
    pdb.set_trace()
    return


def cli_main() -> None:
    input_funcs = [splitstriplines]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, input_funcs)
    answer_one = process_one(data)
    if ANSWER_ONE is not None:
        if answer_one != ANSWER_ONE:
            pdb.set_trace()

        assert answer_one == ANSWER_ONE
    print("Answer one:", answer_one)
    if ANSWER_ONE is not None:
        answer_two = process_two(data)
        if ANSWER_TWO is not None:
            if answer_two != ANSWER_TWO:
                pdb.set_trace()
            assert answer_two == ANSWER_TWO
        print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
