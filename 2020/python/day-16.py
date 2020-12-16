import pdb
import subprocess
from collections import Counter, defaultdict
from functools import partial, reduce, wraps
from itertools import count, groupby
from math import prod
from operator import itemgetter, methodcaller, mul
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
    valfilter,
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
make_incrementer = lambda start=0, step=1: partial(next, count(start, step))


testdata1 = "\n".join(
    [
        "class: 1-3 or 5-7",
        "row: 6-11 or 33-44",
        "seat: 13-40 or 45-50",
        "",
        "your ticket:",
        "7,1,14",
        "",
        "nearby tickets:",
        "7,3,47",
        "40,4,50",
        "55,2,20",
        "38,6,12",
    ]
)

testdata2 = "\n".join(
    [
        "class: 0-1 or 4-19",
        "row: 0-5 or 8-19",
        "seat: 0-13 or 16-19",
        "",
        "your ticket:",
        "11,12,13",
        "",
        "nearby tickets:",
        "3,9,18",
        "15,1,5",
        "5,14,9",
    ]
)


def lnoncontinuous(array: list[int]):
    return lmap(list, noncontinuous(array))


def parse_rules(rules: List[str]):
    d1 = {
        x[0]: x[1]
        for x in map(lambda y: y.split(": "), splitstrip(rules, "\n"))
    }
    d2 = valmap(lambda x: [z for z in splitstrip(x, "or")], d1)

    def storange(s):
        splitx = methodcaller("split", "-")
        toint = compose_left(splitx, c_lmap(str.strip), c_lmap(int))
        return lmap(toint, s)

    return valmap(storange, d2)


def parse_ticket(line: str):
    return lmap(int, splitstrip(line, ","))


def validate_ranges(ranges, value):
    valid = False
    for l, u in ranges:
        if l <= value <= u:
            valid = True
    return valid, value


def validate_ranges2(ranges, value):
    valid = False
    for l, u in ranges:
        if l <= value <= u:
            valid = True
    return valid


def valid_range(rnge, value):
    valid = False
    for l, u in rnge:
        if l <= value <= u:
            valid = True
    return valid


def validate_rules(rules, values):
    valid_for_rules = []
    for rule in rules:
        if all([validate_ranges2(rules[rule], v) for v in values]):
            valid_for_rules.append(rule)
    return valid_for_rules


def validate_ticket(rules, ticket):
    pass


def validate_tickets(rules, nearby):
    valid = []
    invalid = []
    for ticket in nearby:
        invalid_in_ticket = []
        for num in ticket:
            results = [validate_ranges(rnge, num) for rnge in rules.values()]
            if all([not x[0] for x in results]):
                invalid.append(num)
                invalid_in_ticket.append(num)
        if not invalid_in_ticket:
            valid.append(ticket)

    return valid, [], invalid


def process_input(text: str):
    rules, yours, nearby = text.split("\n\n")
    drules = parse_rules(rules)
    lyours = parse_ticket(yours.splitlines()[1])
    lnearby = lmap(parse_ticket, nearby.splitlines()[1:])
    return (drules, lyours, lnearby)


def load_input(fname):
    raw = Path(fname).read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    return raw


def process(data):
    rules, yours, nearby = data
    valid, invalid, invalid_values = validate_tickets(rules, nearby)
    return sum(invalid_values)


def solve_mapping(rules: dict, mapped: dict):
    newmap = defaultdict(list)
    potential = rules.keys()
    while len(list(newmap.keys())) != len(list(potential)):
        only_one = valfilter(lambda x: len(x) == 1, mapped)
        for k, v in only_one.items():
            newmap[v[0]].append(k)
            mapped = valmap(lambda x: [_ for _ in x if _ != v[0]], mapped)
    return newmap


def interpret_tickets(rules, tickets):
    by_column = list(zip(*tickets))
    mapping = {}
    for i, col in enumerate(by_column):
        validity = validate_rules(rules, col)
        if validity:
            mapping[i] = validity

    key = solve_mapping(rules, mapping)

    return key


def process2(data):
    rules, yours, nearby = data
    valid, invalid, invalid_values = validate_tickets(rules, nearby)
    interpreted = interpret_tickets(rules, valid)
    departure_fields = keyfilter(
        lambda x: x.startswith("departure"), interpreted
    )
    answer = reduce(mul, [yours[f[0]] for f in departure_fields.values()])

    return answer


def cli_main():
    data = compose_left(load_input, process_input)("input-16.txt")
    # testanswer = process(process_input(testdata1))
    # testanswer2 = process2(process_input(testdata2))
    # pdb.set_trace()
    answer_one = process(data)
    assert answer_one == 23115
    print("Answer one:", answer_one)

    answer_two = process2(data)
    assert answer_two == 239727793813
    print("Answer two:", answer_two)


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer
    cli_main()
