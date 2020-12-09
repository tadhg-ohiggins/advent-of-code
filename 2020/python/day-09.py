from functools import partial
from pathlib import Path
from typing import Any, Callable, List, Iterable, Optional, Union
from toolz import (  # type: ignore
    compose_left,
    sliding_window,
)


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lcompact = partial(lfilter, None)


def is_sum_in(arr, target):
    for i in arr:
        if target - i in arr:
            return True
    return False


def is_sum_in_prior_n(arr, limit):
    for sw in sliding_window(limit + 1, arr):
        opts = sw[:limit]
        targ = sw[limit]
        if not is_sum_in(opts, targ):
            return targ


def contig_sum(arr, targ):
    sm = 0
    for i, val in enumerate(arr):
        sm = sm + val
        if sm == targ:
            return arr[: i + 1]
    return None


def narrow_array(lines, targ):
    for i in range(0, len(lines)):
        retval = contig_sum(lines[i:], targ)
        if retval:
            return min(retval) + max(retval)


def process(text):
    lines = [int(_) for _ in lcompact(text.splitlines())]
    ans = is_sum_in_prior_n(lines, 25)
    assert ans == 104054607
    print("Answer one:", ans)
    ans2 = narrow_array(lines, ans)
    assert ans2 == 13935797
    print("Answer two:", ans2)
    return


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer

    raw = Path("input-09.txt").read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    result = process(raw)
