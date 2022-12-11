from collections import Counter
from functools import partial, cache
import math
import re

from toolz import pipe, pluck

from tutils import splitblocks
from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    lcompact,
    lmap,  # A version of map that returns a list.
    splitstriplines,
    splitstrip,
)

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
        True: int(splitstrip(lines[4], sep="throw to monkey")[1]),
        False: int(splitstrip(lines[5], sep="throw to monkey")[1]),
    }
    return (monkey_number, data)


def monkey_dict(blocks):
    return {k[0]: k[1] for k in blocks}


@cache
def do_op(opstr, value):
    opstr = opstr.replace("old", str(value))
    op = "+" if "+" in opstr else "*"
    func = sum if op == "+" else math.prod
    return func(map(int, splitstrip(opstr, sep=op)))


def div_worry(worry: int) -> int:
    return math.floor(worry / 3)


@cache
def mod_worry(divisor: int, worry: int) -> int:
    return worry % divisor


@cache
def check(divisor: int, value: int) -> bool:
    return (value % divisor) == 0


def preprocess(data):
    procs = [
        splitblocks,
        partial(lcompact),
        cmap(parse_block),
        monkey_dict,
    ]
    return pipe(data, *procs)


def part_one(monkeys):
    counts, turn = Counter({k: 0 for k in monkeys}), 0

    while turn < 20:
        for monkey_id, monkey in monkeys.items():
            for item in monkey["items"]:
                counts[monkey_id] += 1

                worry = do_op(monkey["operation"], item)
                worry = div_worry(worry)

                key = check(monkey["test"], worry)
                target = monkeys[monkey[key]]
                target["items"].append(worry)

            monkey["items"] = []
        turn = turn + 1

    return math.prod(sorted(counts.values())[-2:])


def part_two(monkeys):
    counts, turn = Counter({k: 0 for k in monkeys}), 0
    product = math.prod(pluck("test", monkeys.values()))
    manage_worry = partial(mod_worry, product)

    while turn < 10000:
        for monkey_id, monkey in monkeys.items():
            for item in monkey["items"]:
                counts[monkey_id] += 1

                worry = do_op(monkey["operation"], item)
                worry = manage_worry(worry)

                key = check(monkey["test"], worry)
                target = monkeys[monkey[key]]
                target["items"].append(worry)

            monkey["items"] = []
        turn = turn + 1

    return math.prod(sorted(counts.values())[-2:])
