from collections import defaultdict
from functools import partial, reduce
from operator import mul
from pathlib import Path
from typing import Any, Callable, List, Iterable, Tuple
from more_itertools import partition
from toolz import (  # type: ignore
    compose_left,
    concat,
    curry,
    keyfilter,
    valfilter,
    valmap,
)


IterableS = Iterable[str]


def omit(remove: IterableS, d: dict) -> dict:
    return {k: d[k] for k in d if k not in remove}


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
c_map = curry(map)
c_lmap = curry(lmap)
lcompact = partial(lfilter, None)
lstrip = partial(lmap, str.strip)
splitstrip = compose_left(str.split, lstrip, lcompact)
splitstriplines = compose_left(str.splitlines, lstrip, lcompact)
seq_to_dict = compose_left(lmap, dict)


def split_to_dict(seq: List, **kwds: Any) -> dict:
    return seq_to_dict(partial(splitstrip, **kwds), seq)


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


def parse_rules(text: str) -> dict:
    split_or = partial(splitstrip, sep="or")
    split_dash_to_int = compose_left(partial(splitstrip, sep="-"), c_lmap(int))
    split_dashes = partial(lmap, split_dash_to_int)
    return compose_left(
        splitstriplines,
        partial(split_to_dict, sep=":"),
        partial(valmap, split_or),
        partial(valmap, split_dashes),
    )(text)


def parse_ticket(line: str) -> List[int]:
    return lmap(int, splitstrip(line, ","))


def valid_range(ranges: List[List[int]], value: int) -> bool:
    return any([low <= value <= high for low, high in ranges])


def validate_rules(rules: dict, values: List[int]) -> List[str]:
    valid = lambda x: all([valid_range(rules[x], v) for v in values])
    return lfilter(valid, rules.keys())


def is_num_in_any_valid_range(rules: dict, num: int) -> bool:
    return any([valid_range(rnge, num) for rnge in rules.values()])


def validate_tickets(rules: dict, nearby: List[str]) -> Tuple:
    valid_tickets = []
    invalid_numbers = []
    for ticket in nearby:
        check = lambda n: not is_num_in_any_valid_range(rules, n)
        not_valid = lfilter(check, ticket)
        if not_valid:
            invalid_numbers.extend(not_valid)
        else:
            valid_tickets.append(ticket)
    return valid_tickets, [], [], invalid_numbers


def validate_ticket(rules: dict, ticket: List[int]) -> Tuple[bool, List, List]:
    check = lambda n: is_num_in_any_valid_range(rules, n)
    invalid_nums, valid_nums = lmap(list, partition(check, ticket))
    valid = not invalid_nums
    return valid, valid_nums, invalid_nums


def fvalidate_tickets(rules: dict, nearby: List[str]) -> Tuple:
    # So much more verbose to not do this imperatively
    validator = partial(validate_ticket, rules)
    validated = lmap(validator, nearby)
    invalid, valid = lmap(list, partition(lambda x: x[0], validated))
    valid_tickets = [_[1] for _ in valid]
    invalid_tickets = [_[1] + _[2] for _ in invalid]
    invalid_nums = list(concat([_[2] for _ in invalid]))
    valid_nums = list(concat([_[1] for _ in valid]))
    return valid_tickets, invalid_tickets, valid_nums, invalid_nums


def process_input(text: str) -> Tuple:
    rules, yours, nearby = splitstrip(text, "\n\n")
    drules = parse_rules(rules)
    lyours = parse_ticket(yours.splitlines()[1])
    lnearby = lmap(parse_ticket, nearby.splitlines()[1:])
    return (drules, lyours, lnearby)


def load_input(fname: str) -> str:
    raw = Path(fname).read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    return raw


def process(data: Tuple) -> int:
    rules, _, nearby = data
    invalid_values = validate_tickets(rules, nearby)[-1]
    return sum(invalid_values)


def solve_mapping(rules: dict, mapped: dict) -> dict:
    columns_to_fields: dict = defaultdict(list)
    num_keys = len(list(rules.keys()))
    while len(list(columns_to_fields.keys())) != num_keys:
        only_one = valfilter(lambda x: len(x) == 1, mapped)
        # pylint: disable=cell-var-from-loop
        for k, v in only_one.items():
            columns_to_fields[v[0]].append(k)
            remove_v_from_list = partial(lfilter, lambda x: x != v[0])
            mapped = valmap(remove_v_from_list, mapped)
        # pylint: enable=cell-var-from-loop
    return columns_to_fields


def columns_with_possible_keys(rules: dict, tickets: List[List[int]]) -> dict:
    columns = list(zip(*tickets))
    valid_keys = partial(validate_rules, rules)
    return {i: x for i, col in enumerate(columns) if (x := valid_keys(col))}


def interpret_tickets(rules: dict, tickets: List[List[int]]) -> dict:
    mapping = columns_with_possible_keys(rules, tickets)
    return solve_mapping(rules, mapping)


def process2(
    data: Tuple, fieldfunc: Callable = lambda x: x.startswith("departure")
) -> int:
    rules, yours, nearby = data
    valid = validate_tickets(rules, nearby)[0]
    interpreted = interpret_tickets(rules, valid)
    departure_fields = keyfilter(fieldfunc, interpreted)
    answer = reduce(mul, [yours[f[0]] for f in departure_fields.values()])

    return answer


def cli_main() -> None:
    testanswer1 = compose_left(process_input, process)(testdata1)
    assert testanswer1 == 71

    data = compose_left(load_input, process_input)("input-16.txt")

    answer_one = process(data)
    assert answer_one == 23115
    print("Answer one:", answer_one)

    testanswer2 = process2(process_input(testdata2), fieldfunc=lambda x: True)
    assert testanswer2 == 1716

    answer_two = process2(data)
    assert answer_two == 239727793813
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
