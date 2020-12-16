import subprocess
from collections import defaultdict
from functools import partial, reduce
from itertools import count, groupby
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
    keyfilter,
    pluck,
    valfilter,
    valmap,
)


IterableS = Iterable[str]


def omit(remove: IterableS, d: dict) -> dict:
    return {k: d[k] for k in d if k not in remove}


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
c_map = curry(map)
lcompact = partial(lfilter, None)
splitstrip = compose_left(str.split, partial(lmap, str.strip), lcompact)
splitstriplines = compose_left(
    str.splitlines, partial(lmap, str.strip), lcompact
)


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


def parse_rules(rules: str):
    split_kv = lambda x: x.split(": ")
    split_or = lambda x: (x[0], splitstrip(x[1], "or"))
    split_dash = lambda y: lmap(int, splitstrip(y, "-"))
    split_dashes = lambda x: (x[0], lmap(split_dash, x[1]))
    procs = compose_left(
        splitstriplines,
        c_map(split_kv),
        c_map(split_or),
        c_map(split_dashes),
        dict,
    )
    return procs(rules)


def parse_ticket(line: str):
    return lmap(int, splitstrip(line, ","))


def valid_range(ranges, value):
    return any([low <= value <= high for low, high in ranges])


def validate_rules(rules: dict, values: List[int]):
    valid = lambda x: all([valid_range(rules[x], v) for v in values])
    return lfilter(valid, rules.keys())


def is_num_in_any_valid_range(rules: dict, num: int) -> bool:
    return any([valid_range(rnge, num) for rnge in rules.values()])


def validate_tickets(rules, nearby):
    valid_tickets = []
    invalid_numbers = []
    for ticket in nearby:
        check = lambda n: not is_num_in_any_valid_range(rules, n)
        not_valid = lfilter(check, ticket)
        if not_valid:
            invalid_numbers.extend(not_valid)
        else:
            valid_tickets.append(ticket)
    return valid_tickets, [], invalid_numbers


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
    rules, _, nearby = data
    _, _, invalid_values = validate_tickets(rules, nearby)
    return sum(invalid_values)


def solve_mapping(rules: dict, mapped: dict):
    newmap: dict = defaultdict(list)
    num_keys = len(list(rules.keys()))
    while len(list(newmap.keys())) != num_keys:
        only_one = valfilter(lambda x: len(x) == 1, mapped)
        for k, v in only_one.items():
            newmap[v[0]].append(k)
            remove_v_from_list = partial(lfilter, lambda x: x != v[0])
            mapped = valmap(remove_v_from_list, mapped)
    return newmap


def columns_with_possible_keys(rules, tickets):
    columns = list(zip(*tickets))
    valid_keys = partial(validate_rules, rules)
    return {i: x for i, col in enumerate(columns) if (x := valid_keys(col))}


def interpret_tickets(rules, tickets):
    mapping = columns_with_possible_keys(rules, tickets)
    return solve_mapping(rules, mapping)


def process2(data):
    rules, yours, nearby = data
    valid, _, _ = validate_tickets(rules, nearby)
    interpreted = interpret_tickets(rules, valid)
    is_departure_field = lambda x: x.startswith("departure")
    departure_fields = keyfilter(is_departure_field, interpreted)
    answer = reduce(mul, [yours[f[0]] for f in departure_fields.values()])

    return answer


def cli_main():
    testanswer1 = compose_left(process_input, process)(testdata1)
    assert testanswer1 == 71

    data = compose_left(load_input, process_input)("input-16.txt")
    answer_one = process(data)
    assert answer_one == 23115
    print("Answer one:", answer_one)

    answer_two = process2(data)
    assert answer_two == 239727793813
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
