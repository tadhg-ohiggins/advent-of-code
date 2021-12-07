from functools import cache, partial, reduce
import aoc
from tadhg_utils import lmap, splitstrip


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 5934
TA2 = 26984457539
A1 = 374927
A2 = 1687617803407


@cache
def twofish(days: int) -> int:
    return 1 if days < 9 else twofish(days - 9) + twofish(days - 7)


def bluefish(days: int, data: list[int]):
    def reducer(acc, val):
        return acc + twofish(days + (8 - val))

    return reduce(reducer, data, 0)


def process_one(data: list[int]):
    return bluefish(80, data)


def process_two(data: list[int]):
    return bluefish(256, data)


def cli_main() -> None:
    input_funcs = [partial(splitstrip, sep=","), partial(lmap, int)]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    result_two = process_two(data)
    aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
