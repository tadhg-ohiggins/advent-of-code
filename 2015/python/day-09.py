from functools import cache, partial, reduce
import pdb
import aoc
from tadhg_utils import lmap, splitstrip, splitstriplines


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 605
TA2 = None
A1 = None
A2 = None


def process_one(data):
    pdb.set_trace()
    return data


def process_two(data):
    pdb.set_trace()
    return data


def cli_main() -> None:
    input_funcs = [splitstriplines]
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
