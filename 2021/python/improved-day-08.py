from collections import Counter
from functools import cache, partial, reduce
import pdb
import aoc
from tadhg_utils import (
    compactd,
    filter_az,
    item_has,
    lconcat,
    lfilter,
    lmap,
    pick,
    splitstrip,
    splitstriplines,
)
from toolz import compose_left, keyfilter


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 26
TA2 = 61229
A1 = 532
A2 = None


NUMS = {
    0: ["aaaa", "bb", "cc", "....", "ee", "ff", "gggg"],
    1: ["....", "..", "cc", "....", "..", "ff", "...."],
    2: ["aaaa", "..", "cc", "dddd", "ee", "..", "gggg"],
    3: ["aaaa", "..", "cc", "dddd", "..", "ff", "gggg"],
    4: ["....", "bb", "cc", "dddd", "..", "ff", "...."],
    5: ["aaaa", "bb", "..", "dddd", "..", "ff", "gggg"],
    6: ["aaaa", "bb", "..", "dddd", "ee", "ff", "gggg"],
    7: ["aaaa", "..", "cc", "....", "..", "ff", "...."],
    8: ["aaaa", "bb", "cc", "dddd", "ee", "ff", "gggg"],
    9: ["aaaa", "bb", "cc", "dddd", "..", "ff", "gggg"],
}

NUM_SEGS = {
    2: 1,
    4: 4,
    3: 7,
    7: 8,
}


def parse_line(line):
    raw_signals, raw_value = splitstrip(line, sep=" | ")
    sortjoin = compose_left(sorted, "".join)
    signals = lmap(sortjoin, raw_signals.split())
    value = lmap(sortjoin, raw_value.split())
    return signals, value


def process_one(data):
    values = lconcat([line[1] for line in data])
    return len(lfilter(lambda d: len(d) in NUM_SEGS, values))


def decipher_line(line):
    signals, value = line
    all_chars = lconcat(
        map(partial(filter, lambda x: "." not in x), lconcat(NUMS.values()))
    )
    segments = {}
    base = {NUM_SEGS.get(len(d)): d for d in value + signals}
    known = keyfilter(lambda x: x is not None, base)

    # If it's in 7 not 1 it's a.
    segments["a"] = (set(known[7]) - set(known[1])).pop()
    assert len(segments.keys()) == len(set(segments.values()))

    # If we have a three-letter--i.e. 7--then whatever six-letter is not a
    # superset of it is six
    sixes = set(filter(lambda x: len(x) in (6,), signals))
    for t in sixes:
        if not set(t) >= set(known[7]):
            known[6] = t
            assert len(set(known[7]) - set(known[6])) == 1
            segments["c"] = (set(known[7]) - set(known[6])).pop()

    assert len(segments.keys()) == len(set(segments.values()))

    # Now we know what c is, f is whatever is in 1 that's not a or c:
    ac = list(pick(["a", "c"], segments).values())
    assert len(set(known[1]) - set(ac)) == 1
    segments["f"] = (set(known[1]) - set(ac)).pop()
    assert len(segments.keys()) == len(set(segments.values()))

    # Now we know acf, we know that any signal lacking f is 2:
    twos = lfilter(lambda x: segments["f"] not in x, signals)
    assert len(twos) == 1
    known[2] = twos[0]

    # Now whatever's in 6 that isn't in 7|2 is b:
    seven_u_two = set(known[7]).union(set(known[2]))
    assert len(set(known[6]) - seven_u_two) == 1
    segments["b"] = (set(known[6]) - seven_u_two).pop()
    assert len(segments.keys()) == len(set(segments.values()))

    # Whatever isn't these in four is d:
    four_not_bcf = set(known[4]) - set(
        pick(["b", "c", "f"], segments).values()
    )
    assert len(four_not_bcf) == 1
    segments["d"] = four_not_bcf.pop()
    assert len(segments.keys()) == len(set(segments.values()))

    # eight minus d is zero:
    known[0] = "".join(sorted(filter(lambda x: x != segments["d"], known[8])))

    # nine is whatever six-length signal isn't 0 or 6:
    nine = [x for x in sixes if x not in known.values()]
    assert len(nine) == 1
    known[9] = nine[0]

    # whatever is in 2 but not in 9 is e:
    two_not_nine = set(known[2]) - set(known[9])
    assert len(two_not_nine) == 1
    segments["e"] = two_not_nine.pop()
    assert len(segments.keys()) == len(set(segments.values()))

    # Whatever of the five-length signals contains b is 5:
    fives = set(filter(lambda x: len(x) in (5,), signals))
    five = [x for x in fives if segments["b"] in x]
    assert len(five) == 1
    known[5] = five[0]

    # Whatever five-length isn't 2 or 5 is 3:
    three = [x for x in fives if x not in (known[2], known[5])]
    assert len(three) == 1
    known[3] = three[0]

    # Whatever's in the signal that isn't in segments values must be g:
    leftover = set(all_chars) - set(segments.values())
    assert len(leftover) == 1
    segments["g"] = leftover.pop()

    assert len(known) == 10
    codex = {v: k for k, v in known.items()}
    digits = ""
    for num in value:
        digits = digits + str(codex[num])

    return int(digits, 10)


def process_two(data):
    return sum(map(decipher_line, data))


def cli_main() -> None:
    input_funcs = [splitstriplines, partial(lmap, parse_line)]
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
