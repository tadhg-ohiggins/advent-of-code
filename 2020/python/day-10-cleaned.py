from collections import Counter
from functools import partial
from itertools import groupby
from operator import itemgetter
from pathlib import Path
from toolz import compose_left, sliding_window  # type: ignore


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lcompact = partial(lfilter, None)
splitstrip = compose_left(str.split, partial(lmap, str.strip), lcompact)


def noncontinuous(array: list[int]):
    """
    noncontinuous([1, 2, 3, 5, 6, 8, 9, 10]) == [[1, 2, 3], [5, 6], [8, 9, 10]]

    The difference between a number and its index will be stable for a
    consecutive run, so we can group by that.

    -1 for 1, 2, and 3; -2 for 5 and 6; -3 for 8, 9 and 10 in the above list.

    enumerate gets us item and index, a quick x[0] - x[1] lambda gets us the
    difference.

    Once we have them in groups, we extract them into the lists of runs.

    See also consecutive_groups in more_itertools, which was the basis for
    this.
    """
    check = lambda x: x[0] - x[1]
    collate = lambda x: map(itemgetter(1), list(x)[1])
    return map(collate, groupby(enumerate(array), key=check))


def lnoncontinuous(array: list[int]):
    return lmap(list, noncontinuous(array))


def find_combos(length):
    """
    In the data, there are no gaps of two, only gapes of one or three, between
    numbers in the sorted list.
    The rules are such that the number of combos are the same regardless
    of the specific numbers involved--there are the same number of combos
    for [0, 1, 2, 3] and for [23, 24, 25, 26].
    So we only need the length of a run to figure out the number of
    combos in it.

    The rule is that any number can be skipped as long as there's not a gap of
    more than three. Since we're dealing with runs that are separated by gaps
    of three, the first and last numbers must be included in each combo.

    So for [0, 1, 2] the only combos are [0, 2] and [0, 1, 2].

    For runs of three, the answer is two. For four, it's four. But at five, you
    hit a limit of having a gap of more than three between the start and
    finish.

    Because the start and finish numbers of each run are required, and gaps of
    more than three aren't allowed, and there are no gaps of two, it looks like
    a run of n has combos equal to the sum of runs of n-1, n-2, n-3.

    n1 = 1
    n2 = 1
    n3 = 2
    n4 = 4
    n5 = 7
    n6 = 13
    """

    start = {0: 0, 1: 1, 2: 1}
    if length in start:
        return start[length]
    return sum(map(find_combos, [max([0, length - _]) for _ in (1, 2, 3)]))


def process(text):
    lines = lmap(int, lcompact(text.splitlines()))
    adapters = sorted(lines)
    total = [0] + adapters + [max(adapters) + 3]
    diffs = Counter([a - b for a, b in sliding_window(2, reversed(total))])

    answer_one = diffs[1] * diffs[3]
    assert answer_one == 2272

    runs = Counter([len(span) for span in lnoncontinuous(total)])
    combos = {k: find_combos(k) for k in runs}
    total = 1
    for combo in combos:
        total = total * combos[combo] ** runs[combo]
    assert total == 84627647627264
    print("Answer one:", answer_one)
    print("Answer two:", total)


if __name__ == "__main__":
    process(Path("input-10.txt").read_text().strip())
