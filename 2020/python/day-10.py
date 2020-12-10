from functools import partial, reduce, wraps
from pathlib import Path
from typing import Any, Callable, List, Iterable, Optional, Sequence, Union
from toolz import (  # type: ignore
    compose_left,
    sliding_window,
)


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lcompact = partial(lfilter, None)
splitstrip = compose_left(str.split, partial(lmap, str.strip), lcompact)


def process(text):
    lines = lmap(int, lcompact(text.splitlines()))
    adapters = sorted(lines)
    total = [0] + adapters + [max(adapters) + 3]
    differences = {0: 0, 1: 0, 2: 0, 3: 0}
    for jolt_h, jolt_l in sliding_window(2, reversed(total)):
        diff = jolt_h - jolt_l
        differences[diff] = differences[diff] + 1

    answer_one = differences[1] * differences[3]
    assert answer_one == 2272

    running, guess = 0, 1
    factors = {3: 2, 4: 4, 5: 7}
    for i in range(len(total)):
        if i == len(total):
            break
        if i > 0:
            if total[i] - total[i - 1] == 3:
                span = total[running:i]
                if len(span) in factors:
                    guess = guess * factors[len(span)]
                running = i
    assert guess == 84627647627264
    print("Answer one:", answer_one)
    print("Answer two:", guess)

    return


if __name__ == "__main__":
    process(Path("input-10.txt").read_text().strip())
