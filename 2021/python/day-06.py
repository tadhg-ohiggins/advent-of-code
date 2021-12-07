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
"""
--- Day 6: Lanternfish ---

The sea floor is getting steeper. Maybe the sleigh keys got carried this way?

A massive school of glowing lanternfish swims past. They must spawn quickly to
reach such large numbers - maybe exponentially quickly? You should model their
growth rate to be sure.

Although you know nothing about this specific species of lanternfish, you make
some guesses about their attributes. Surely, each lanternfish creates a new
lanternfish once every 7 days.

However, this process isn't necessarily synchronized between every lanternfish
- one lanternfish might have 2 days left until it creates another lanternfish,
while another might have 4. So, you can model each fish as a single number that
represents the number of days until it creates a new lanternfish.

Furthermore, you reason, a new lanternfish would surely need slightly longer
before it's capable of producing more lanternfish: two more days for its first
cycle.

So, suppose you have a lanternfish with an internal timer value of 3:

    After one day, its internal timer would become 2.
    After another day, its internal timer would become 1.
    After another day, its internal timer would become 0.
    After another day, its internal timer would reset to 6,
        and it would create a new lanternfish with an internal timer of 8.
    After another day, the first lanternfish would have an internal timer of 5,
        and the second lanternfish would have an internal timer of 7.

A lanternfish that creates a new fish resets its timer to 6, not 7 (because 0
is included as a valid timer value). The new lanternfish starts with an
internal timer of 8 and does not start counting down until the next day.

Realizing what you're trying to do, the submarine automatically produces a list
of the ages of several hundred nearby lanternfish (your puzzle input). For
example, suppose you were given the following list:

3,4,3,1,2

This list means that the first fish has an internal timer of 3, the second fish
has an internal timer of 4, and so on until the fifth fish, which has an
internal timer of 2. Simulating these fish over several days would proceed as
follows:

Initial state: 3,4,3,1,2
After  1 day:  2,3,2,0,1
After  2 days: 1,2,1,6,0,8
After  3 days: 0,1,0,5,6,7,8
After  4 days: 6,0,6,4,5,6,7,8,8
After  5 days: 5,6,5,3,4,5,6,7,7,8
After  6 days: 4,5,4,2,3,4,5,6,6,7
After  7 days: 3,4,3,1,2,3,4,5,5,6
After  8 days: 2,3,2,0,1,2,3,4,4,5
After  9 days: 1,2,1,6,0,1,2,3,3,4,8
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8

Each day, a 0 becomes a 6 and adds a new 8 to the end of the list, while each
other number decreases by 1 if it was present at the start of the day.

In this example, after 18 days, there are a total of 26 fish. After 80 days,
there would be a total of 5934.

Find a way to simulate lanternfish. How many lanternfish would there be after
80 days?

Your puzzle answer was 374927.
--- Part Two ---

Suppose the lanternfish live forever and have unlimited food and space. Would
they take over the entire ocean?

After 256 days in the example above, there would be a total of 26984457539
lanternfish!

How many lanternfish would there be after 256 days?

Your puzzle answer was 1687617803407.
"""
