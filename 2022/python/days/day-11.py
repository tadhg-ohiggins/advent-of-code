from functools import partial, cache
from itertools import permutations
from string import ascii_lowercase, ascii_uppercase
import math
import re

from more_itertools import chunked
from toolz import (
    compose_left,
    pipe,
    sliding_window,
)

from tutils import trace, splitblocks
from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    lcompact,
    lfilter,
    lmap,  # A version of map that returns a list.
    splitstriplines,
    splitstrip,
    star,
)
import pdb


TEST_ANSWERS = (10605, 2713310158)
PUZZLE_ANSWERS = (113220, 30599555965)


def parse_block(block):
    lines = splitstriplines(block)
    monkey_number = int(re.findall(r"\d+", lines[0])[0])
    items_str = splitstrip(lines[1], sep=":")[1]
    operation = splitstrip(lines[2], sep="=")[1]

    # items = lmap(int, splitstrip(items_str))
    data = {
        "monkey": monkey_number,
        "items": lmap(int, splitstrip(items_str, sep=",")),
        "operation": operation,
        "test": int(splitstrip(lines[3], sep="divisible by")[1]),
        "test_true": int(splitstrip(lines[4], sep="throw to monkey")[1]),
        "test_false": int(splitstrip(lines[5], sep="throw to monkey")[1]),
    }
    return (monkey_number, data)


def monkey_dict(blocks):
    return {k[0]: k[1] for k in blocks}


def preprocess(data):
    procs = [
        splitblocks,
        partial(lcompact),
        cmap(parse_block),
        monkey_dict,
    ]
    result = pipe(data, *procs)
    return result


def part_one(primates):
    monkeys = {**primates}

    counts = {k: 0 for k in monkeys}
    turn = 0

    while turn < 20:
        for mid in sorted(monkeys.keys()):
            mkey = monkeys[mid]
            to_delete = []
            for item in mkey["items"]:
                counts[mid] = counts[mid] + 1

                worry = item
                op = mkey["operation"].replace("old", str(worry))
                worry = eval(op)
                worry = math.floor(worry / 3)

                if worry % mkey["test"] == 0:
                    target = mkey["test_true"]
                    monkeys[target]["items"].append(worry)
                    if target != mid:
                        to_delete.append(item)
                else:
                    target = mkey["test_false"]
                    monkeys[target]["items"].append(worry)
                    if target != mid:
                        to_delete.append(item)
            for gone in to_delete:
                mkey["items"].remove(gone)
        turn = turn + 1

    return math.prod(sorted(counts.values())[-2:])


def get_worry(opstr, all_evals, test, tests, worry):
    return worry % math.prod(tests)


def part_two(monkeys):
    counts = {k: 0 for k in monkeys}
    all_tests = [monkeys[m]["test"] for m in monkeys]
    all_evals = [monkeys[m]["operation"] for m in monkeys]
    turn = 0

    while turn < 10000:
        for mid in sorted(monkeys.keys()):
            mkey = monkeys[mid]
            to_delete = []
            for item in mkey["items"]:
                counts[mid] = counts[mid] + 1

                worry = item
                op = mkey["operation"].replace("old", str(worry))
                worry = eval(op)

                if worry % mkey["test"] == 0:
                    target = monkeys[mkey["test_true"]]

                    worry = get_worry(
                        target["operation"],
                        all_evals,
                        target["test"],
                        all_tests,
                        worry,
                    )
                    target["items"].append(worry)
                    to_delete.append(item)
                else:
                    target = monkeys[mkey["test_false"]]
                    worry = get_worry(
                        target["operation"],
                        all_evals,
                        target["test"],
                        all_tests,
                        worry,
                    )
                    target["items"].append(worry)
                    to_delete.append(item)
            for gone in to_delete:
                mkey["items"].remove(gone)
        turn = turn + 1

    return math.prod(sorted(counts.values())[-2:])
