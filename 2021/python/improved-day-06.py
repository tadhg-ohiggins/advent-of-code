from functools import cache, partial
import aoc
from tadhg_utils import lmap, splitstrip


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 5934
TA2 = 26984457539
A1 = 374927
A2 = 1687617803407


@cache
def twofish(daycount):
    if daycount >= 9:
        return twofish(daycount - 9) + twofish(daycount - 7)
    return 1


def redfish(daycount, data):
    count = 0
    for n in data:
        count = count + twofish(daycount + (8 - n))
    return count


def process_one(data):
    return redfish(80, data)


def process_two(data):
    return redfish(256, data)


def cli_main() -> None:
    input_funcs = [partial(splitstrip, sep=","), partial(lmap, int)]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    result_two = process_two(data)
    aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
