from collections import Counter
from functools import cache, partial
from itertools import starmap
import math
import pdb
from toolz import compose_left
import aoc
from tadhg_utils import (
    get_sign,
    lcompact,
    lconcat,
    lmap,
    splitstrip,
    splitstriplines,
)


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 5934
TA2 = 26984457539
A1 = 374927
A2 = 1687617803407


def day(fish):
    new_fish = []
    for fishy in fish:
        if fishy > 0:
            new_fishy = fishy - 1
            new_fish.append(new_fishy)
        else:
            new_fish.append(6)
            new_fish.append(8)
    return new_fish


def days(days, data):
    for i in range(days):
        data = day(data)

    return data


"""
If you take a new fish (one that will spawn in 8 days and then 6 days
thereafter) the set of fish you have after n days is the same as the set after
n -9 days plus the set after n -7 days.

Since the sets of fish are always the same you can use that fact to ignore the
sets entirely and just count the number of fish in the sets.

Also, any fish/day combo can be made into a "new fish" by changing the number
of days, essentially backdating the fish to when it had 8 days left. And then
generating the total number of fish becomes a matter of looking at the initial
set and backdating each fish in that set so that the count of days for that
"family" of fish starts from when the original fish had 8 days left.

E.g. the final total number of fish generated in 30 days by a fish starting
with a count of 3 is the same as the number of fish generated in 35 days by a
fish starting with a count of 8.
"""


@cache
def twofish(daycount):
    if daycount >= 16:
        return twofish(daycount - 9) + twofish(daycount - 7)
    if daycount < 9:
        return 1
    if daycount < 16:
        return 2
    return 0


def redfish(daycount, data):
    count = 0
    for n in data:
        count = count + twofish(daycount + (8 - n))
    return count


def process_one(data):
    for i in range(80):
        data = day(data)

    return len(data)


def process_two(data):
    count = 0
    for n in data:
        count = count + twofish(256 + (8 - n))
    return count


def cli_main() -> None:
    input_funcs = [partial(splitstrip, sep=","), partial(lmap, int)]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    result_two = process_two(data)
    aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
