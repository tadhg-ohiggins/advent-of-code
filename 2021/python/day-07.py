from functools import cache, partial, reduce
import pdb
import aoc
from tadhg_utils import lmap, splitstrip


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 37
TA2 = 168
A1 = 331067
A2 = 92881128


def get_cost(candidate, position):
    return abs(position - candidate)


def get_cost_two(candidate, position):
    base = abs(position - candidate)
    steps = sum(range(base + 1))
    return steps


def process_one(data):
    viable_positions = range(min(data), max(data) + 1)
    lowest = None
    for viable_position in viable_positions:
        costs = sum([get_cost(viable_position, position) for position in data])
        if lowest is None:
            lowest = costs
        elif costs < lowest:
            lowest = costs
    return lowest


def process_two(data):
    viable_positions = range(min(data), max(data) + 1)
    lowest = None
    for viable_position in viable_positions:
        costs = sum(
            [get_cost_two(viable_position, position) for position in data]
        )
        if lowest is None:
            lowest = costs
        elif costs < lowest:
            lowest = costs
    return lowest


def cli_main() -> None:
    input_funcs = [partial(splitstrip, sep=","), partial(lmap, int)]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    print(result_one)
    result_two = process_two(data)
    aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
"""
"""
