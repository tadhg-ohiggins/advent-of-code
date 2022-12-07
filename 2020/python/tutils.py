from __future__ import annotations
import json
import pdb
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from functools import partial, reduce, singledispatch, wraps
from itertools import count, groupby, product
from math import prod
from operator import itemgetter, methodcaller
from pathlib import Path
from pprint import pprint
from string import (
    ascii_lowercase,
    digits as ascii_digits,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Iterable,
    Iterator,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)


from toolz import (  # type: ignore
    accumulate,
    compose_left,
    concat,
    curry,
    do,
    excepts,
    flip,
    identity,
    iterate,
    juxt,
    keyfilter,
    mapcat,
    partitionby,
    pluck,
    pipe,
    sliding_window,
    unique,
    valfilter,
    valmap,
)


# pylint: disable=unsubscriptable-object
Json = Union[list, dict]
IterableS = Iterable[str]
DT = datetime
OAny = Optional[Any]
OInt = Optional[int]
ODict = Optional[dict]
OList = Optional[List]
OSet = Optional[Set]
OStr = Optional[Set]
UBoolInt = Union[bool, int]
UBoolList = Union[bool, list]
UListStr = Union[list, str]
UCall = Union[Callable, partial]
OUCall = Optional[UCall]
UListCall = Union[List[UCall], List[Callable], List[partial]]
# pylint: enable=unsubscriptable-object
hexc = ["a", "b", "c", "d", "e", "f"] + list(ascii_digits)


# Sequences
from tadhg_utils import (
    add_debug,
    add_debug_list,
    c_lmap,
    c_map,
    compact,
    excepts_wrap,
    filter_az,
    filter_az09,
    filter_hex,
    filter_str,
    from_8601,
    is_char_09,
    is_char_az,
    is_char_az09,
    is_char_hex,
    item_has,
    lcompact,
    lconcat,
    lfilter,
    lmap,
    lnoncontinuous,
    lpluck,
    noncontinuous,
    oxford,
    make_incrementer,
    nextwhere,
    split_to_dict,
    splitstrip,
    splitstriplines,
    strip_each as lstrip,
    until_stable,
)


def make_list(arr: Any) -> List:
    return [*arr] if isinstance(arr, list) else [arr]


def list_accumulator(itr: Iterable) -> Iterable[List]:
    # list(list_accumulator([1, 2, 3]) -> [[1], [1, 2], [1, 2, 3]]
    return filter(
        None, accumulate(lambda a, b: make_list(a) + make_list(b), itr, [])
    )


# /Sequences


# Misc
def in_incl_range(lower: float, upper: float, candidate: float) -> bool:
    return lower <= candidate <= upper


def run_process(
    command: UListStr, options: ODict = None
) -> subprocess.CompletedProcess:
    base_opts = {"check": True, "text": True, "capture_output": True}
    opts = options if options else {}
    # pylint: disable=subprocess-run-check
    # return subprocess.run(command, **{**base_opts, **opts})  # type: ignore
    return subprocess.run(command, **(base_opts | opts))  # type: ignore


# /Misc

# Coordinates
@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        # Point(1,
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, other: int) -> Point:
        return Point(x=self.x * other, y=self.y * other)

    def __iter__(self) -> Iterable:
        return iter([self.x, self.y])

    @classmethod
    def from_string(cls, raw_point):
        # From e.g. "5,23" to Point(x=5, y=23)
        no_parens = raw_point.replace("(", "").replace(")", "")
        return cls(*map(int, splitstrip(no_parens, sep=",")))


def adjacent_transforms(
    dimensions: int, omit_origin: bool = True
) -> List[Tuple]:
    adj = product([-1, 0, 1], repeat=dimensions)
    not_origin = lambda x: not all([_ == 0 for _ in x])
    return lfilter(not_origin, adj) if omit_origin else adj


def get_min_max_bounds_from_coords(
    coords: Iterable[Tuple],
) -> Tuple[List[int], List[int]]:
    dimensions = len(next(iter(coords)))
    minimums, maximums = [0] * dimensions, [0] * dimensions

    # AFAICT an iterative approach is faster than recursive approaches
    for point in coords:
        for i, number in enumerate(point):
            if number > maximums[i]:
                maximums[i] = number
            if number < minimums[i]:
                minimums[i] = number
    return minimums, maximums


def generate_bounded_coords(
    minimums: List[int], maximums: List[int]
) -> Iterable[Tuple]:
    # In order to be used as the upper bounds for range, the values in maximums
    # need to be one higher:
    ranges = (range(*_) for _ in zip(minimums, [_ + 1 for _ in maximums]))
    return product(*ranges)


# /Coordinates


# File reading/writing


def load_text(fname: Union[Path, str]) -> str:
    return Path(fname).read_text()


def load_json(fname: Union[Path, str]) -> Json:
    return json.loads(load_text(fname))


def write_path_with_text(fname: Path, text: str) -> None:
    fname.write_text(text)


def write_path_with_json(fname: Path, data: Json) -> None:
    write_path_with_text(fname, json.dumps(data))


# /File reading/writing


# Advent of Code helpers
def load_and_process_input(
    fname: Union[Path, str], input_funcs: UListCall
) -> Any:
    processinput = partial(process_input, input_funcs)
    return compose_left(load_input, processinput)(fname)


def load_input(fname: str) -> str:
    return Path(fname).read_text()


def process_input(input_funcs: List[Callable], text: str) -> Any:
    return compose_left(*input_funcs)(text)


def get_inputs(fname: str) -> tuple[Path, Path]:
    path = Path(fname)
    day = path.stem[-2:]
    data, testdata = f"input-{day}.txt", f"test-input-{day}.txt"
    return (path.parent / data, path.parent / testdata)


def test(
    testfile: Union[Path, str],
    answer: Any,
    input_funcs: UListCall,
    process: Callable,
    ordinal: int,
) -> None:
    testdata = load_and_process_input(testfile, input_funcs)
    result = process(testdata)
    if result != answer:
        pdb.set_trace()
    print(f"Test answer {ordinal}:", result)


def tests(
    testfile: Union[Path, str],
    tanswer_one: Any,
    tanswer_two: Any,
    answer_one: Any,
    input_funcs: UListCall,
    process_1: Callable,
    process_2: Callable,
) -> Any:
    testdata = load_and_process_input(testfile, input_funcs)
    result = process_1(testdata)
    if result != tanswer_one:
        pdb.set_trace()
    assert result == tanswer_one
    print("Test answer one:", result)
    if answer_one is not None:
        result_two = process_2(testdata)
        if tanswer_two is not None:
            if result_two != tanswer_two:
                pdb.set_trace()
            assert result_two == tanswer_two
            print("Test answer two:", result_two)


def run_tests(
    testfile: Union[Path, str],
    tanswer_one: Any,
    tanswer_two: Any,
    answer_one: Any,
    input_funcs: UListCall,
    process_1: Callable,
    process_2: Callable,
) -> None:
    if Path(testfile).exists():
        test(testfile, tanswer_one, input_funcs, process_1, 1)
        if answer_one is not None and tanswer_two is not None:
            test(testfile, tanswer_two, input_funcs, process_2, 2)
    else:
        testfile_one = f"{Path(testfile).stem}-{1}.txt"
        testfile_two = f"{Path(testfile).stem}-{2}.txt"
        if Path(testfile_one).exists():
            test(testfile_one, tanswer_one, input_funcs, process_1, 1)
        if Path(testfile_two).exists():
            test(testfile_two, tanswer_two, input_funcs, process_2, 2)


def finish(result_one, answer_one, result_two, answer_two):
    try:
        if answer_one is not None:
            assert result_one == answer_one
        print("Answer one:", result_one)
        if answer_two is not None:
            assert result_two == answer_two
        print("Answer two:", result_two)
    except AssertionError:
        pdb.set_trace()


def splitblocks(text):
    return lmap(str.strip, text.split("\n\n"))


# /Advent of Code helpers


def innermap(func, sequence):
    # Assumes that sequences contains elements that are all themselves
    # iterable. lmap will be called on each elements of sequence, with func as
    # the function.
    return lmap(partial(lmap, func), sequence)


def add_trace_list(funcs):
    nfuncs = []
    for func in funcs:
        if func.__qualname__ is None:
            func.__qualname__ = ""
        nfunc = add_trace(func)
        nfuncs.append(nfunc)
    return nfuncs


def add_trace(func):
    @wraps(func)
    def addtrace(arg):
        if hasattr(func, "_partial"):
            funcdata = func._partial
        else:
            funcdata = func.__name__
        pdb.set_trace()
        return func(arg)

    return addtrace


def dpipe(data, *funcs):
    funcs = add_trace_list(funcs)
    return pipe(data, *funcs)
