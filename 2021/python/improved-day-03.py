from typing import Callable
import aoc
from tadhg_utils import lfilter, splitstriplines


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 198
TA2 = 230
A1 = 749376
A2 = 2372923


def get_most_common(array: list) -> str:
    return "1" if array.count("1") >= array.count("0") else "0"


def get_least_common(array: list) -> str:
    return "1" if array.count("1") < array.count("0") else "0"


def process_one(data: list[str]):
    cols = list(zip(*data))
    gamma = "".join(map(get_most_common, cols))
    epsilon = "".join(map(get_least_common, cols))
    return int(gamma, 2) * int(epsilon, 2)


def filter_by_func(func: Callable, lines: list[str]) -> str:
    colnum = 0
    while len(lines) > 1:
        cols = list(zip(*lines))
        qualified = func(cols[colnum])
        lines = lfilter(lambda x: x[colnum] == qualified, lines)
        colnum = colnum + 1
    assert len(lines) == 1
    return lines[0]


def process_two(data: list[str]):
    oxy_line = filter_by_func(get_most_common, data)
    co_line = filter_by_func(get_least_common, data)
    return int(oxy_line, 2) * int(co_line, 2)


def cli_main() -> None:
    input_funcs = [splitstriplines]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    result_two = process_two(data)
    aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
