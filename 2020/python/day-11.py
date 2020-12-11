import json
import pdb
import subprocess
from collections import Counter
from functools import partial, reduce, wraps
from pathlib import Path
from typing import Any, Callable, List, Iterable, Optional, Sequence, Union
from toolz import (  # type: ignore
    compose_left,
    concat,
    do,
    iterate,
)


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lcompact = partial(lfilter, None)
splitstrip = compose_left(str.split, partial(lmap, str.strip), lcompact)


def is_crowded(i, lnum, line, lines):
    llimit, rlimit = 0, len(line) - 1
    ulimit, dlimit = 0, len(lines) - 1
    count = 0
    # print("_-------------_")
    for j in range(lnum - 1, lnum + 2):
        # print("j", j)
        for k in range(i - 1, i + 2):
            if k >= llimit and k <= rlimit and j >= ulimit and j <= dlimit:
                try:
                    if lines[j][k] == "#":
                        if not (j == lnum and k == i):
                            count = count + 1
                except:
                    pdb.set_trace()
            # print("count", count)
    return count >= 4


def is_crowded2(i, lnum, line, lines):
    llimit, rlimit = 0, len(line) - 1
    ulimit, dlimit = 0, len(lines) - 1
    count = 0
    # print("_-------------_")
    for j in range(lnum - 1, lnum + 2):
        # print("j", j)
        for k in range(i - 1, i + 2):
            if k >= llimit and k <= rlimit and j >= ulimit and j <= dlimit:
                try:
                    if lines[j][k] == "#":
                        if not (j == lnum and k == i):
                            count = count + 1
                except:
                    pdb.set_trace()
            # print("count", count)
    return count >= 5


def is_empty(i, lnum, line, lines):
    llimit, rlimit = 0, len(line) - 1
    ulimit, dlimit = 0, len(lines) - 1
    count = 0
    for j in range(lnum - 1, lnum + 2):
        for k in range(i - 1, i + 2):
            if line == "#.LL.L#.##":
                if k >= llimit and k <= rlimit and j >= ulimit and j <= dlimit:
                    print(j, k, lines[j][k])

            if k >= llimit and k <= rlimit and j >= ulimit and j <= dlimit:
                if lines[j][k] == "#":
                    return False
    return True


def process_line(lnum, line, lines):
    newline = []
    for i, c in enumerate(line):
        if c == "L" and is_empty(i, lnum, line, lines):
            newline = newline + ["#"]
        elif c == "#" and is_crowded(i, lnum, line, lines):
            newline = newline + ["L"]
        else:
            newline = newline + [c]
    # print(newline)
    return "".join(newline)


def is_nosight(cnum, lnum, line, lines, sightlines, debug=False):
    if debug:
        pdb.set_trace()
    co = (lnum, cnum)
    cokey = f"{lnum}-{cnum}"
    rings = sightlines[cokey]["rings"]
    blocked = []
    for ring in rings:
        for j, k in ring:
            if not any([b(co, (j, k)) for b in blocked]):
                try:
                    target = lines[j][k]
                except:
                    pdb.set_trace()
                if target == "#":
                    return False
                elif target == "L":
                    newblocked = [b for b in dirs if b(co, (j, k))]
                    blocked = blocked + newblocked
    return True


def is_distance(origin, coords, distance):
    lnum, cnum = origin
    tlnum, tcnum = coords
    absldist = abs(lnum - tlnum)
    if abs(lnum - tlnum) == abs(cnum - tcnum) and absldist == distance:
        return True
    if lnum == tlnum and abs(tcnum - cnum) == distance:
        return True
    if cnum == tcnum and abs(tlnum - lnum) == distance:
        return True
    return False


def is_blocked_south(origin, coords):
    lnum, cnum = origin
    tlnum, tcnum = coords
    return cnum == tcnum and tlnum > lnum


def is_blocked_north(origin, coords):
    lnum, cnum = origin
    tlnum, tcnum = coords
    return cnum == tcnum and tlnum < lnum


def is_blocked_east(origin, coords):
    lnum, cnum = origin
    tlnum, tcnum = coords
    return lnum == tlnum and tcnum > cnum


def is_blocked_west(origin, coords):
    lnum, cnum = origin
    tlnum, tcnum = coords
    return lnum == tlnum and tcnum < cnum


def is_blocked_nw(origin, coords):
    lnum, cnum = origin
    tlnum, tcnum = coords
    return all(
        [
            abs(lnum - tlnum) == abs(cnum - tcnum),
            tlnum < lnum,
            tcnum < cnum,
        ]
    )


def is_blocked_ne(origin, coords):
    lnum, cnum = origin
    tlnum, tcnum = coords
    return all(
        [
            abs(lnum - tlnum) == abs(cnum - tcnum),
            tlnum < lnum,
            tcnum > cnum,
        ]
    )


def is_blocked_se(origin, coords):
    lnum, cnum = origin
    tlnum, tcnum = coords
    return all(
        [
            abs(lnum - tlnum) == abs(cnum - tcnum),
            tlnum > lnum,
            tcnum > cnum,
        ]
    )


def is_blocked_sw(origin, coords):
    lnum, cnum = origin
    tlnum, tcnum = coords
    return all(
        [
            abs(lnum - tlnum) == abs(cnum - tcnum),
            tlnum > lnum,
            tcnum < cnum,
        ]
    )


dirs = [
    is_blocked_south,
    is_blocked_north,
    is_blocked_east,
    is_blocked_west,
    is_blocked_nw,
    is_blocked_ne,
    is_blocked_se,
    is_blocked_sw,
]


def is_sightcrowded(cnum, lnum, line, lines, sightlines):
    if is_crowded2(cnum, lnum, line, lines):
        return True
    count = 0
    co = (lnum, cnum)
    cokey = f"{lnum}-{cnum}"
    if cokey not in sightlines:
        pdb.set_trace()
    blocked = []
    rings = sightlines[cokey]["rings"]

    for ring in rings:
        for j, k in ring:
            if not any([b(co, (j, k)) for b in blocked]):
                target = lines[j][k]
                if target in ("#", "L"):
                    blocked = blocked + [b for b in dirs if b(co, (j, k))]
                if target == "#":
                    count = count + 1
                    if count >= 5:
                        return True

    return count >= 5


def process_line2(lnum, line, lines, sightlines):
    if lnum >= len(lines):
        pdb.set_trace()
    newline = []
    for i, c in enumerate(line):
        if c == "L" and is_nosight(i, lnum, line, lines, sightlines):
            newline = newline + ["#"]
        elif c == "#" and is_sightcrowded(i, lnum, line, lines, sightlines):
            newline = newline + ["L"]
        else:
            newline = newline + [c]
    return "".join(newline)


def process(text):
    lines = lcompact(text.splitlines())
    proc = lambda x: [process_line(i, l, x) for i, l in enumerate(x)]
    # res = [process_line(x) for x in testlines]
    res1 = proc(testlines)
    res2 = proc(res1)
    testr = testlines
    for i in range(10):
        testr = proc(testr)
    assert testr == stable

    """
    while False:
        newsubj = proc(subj)
        if newsubj == subj:
            break
        subj = newsubj
        # pprint(subj)

    cc = Counter(concat(subj))
    assert cc["#"] == 2303
    test_input = [
        block.split("\n")
        for block in Path("test-input-11-b.txt")
        .read_text()
        .strip()
        .split("\n\n")
    ]

    all_coords = sorted(
        [(a, b) for a in range(len(working)) for b in range(len(working[0]))]
    )
    sightlines = {}
    for coords in all_coords:
        j, k = coords
        visible = [point for point in all_coords if is_insight(coords, point)]
        sightlines[f"{j}-{k}"] = {"visible": visible}
    sightlines = json.loads(
        Path("input-11-b-sightlines-rings.json").read_text()
    )
    rings = {k: {"rings": sightlines[k]["rings"]} for k in sightlines}
    """
    """
    for key in sightlines:
        visible = sightlines[key]["visible"]
        sightlines[key]["rings"] = []
        origin = lmap(int, key.split("-"))
        checked = []
        for i in range(1, 101):
            ring = []
            for coords in visible:
                if coords not in checked:
                    if is_distance(origin, coords, i):
                        ring.append(coords)
            if ring:
                sightlines[key]["rings"].append(ring)
    """
    working = lines
    sightlines = json.loads(Path("input-11b-rings.json").read_text())

    proc2 = lambda x: [
        process_line2(i, l, x, sightlines) for i, l in enumerate(x)
    ]
    ff = working
    ccount = 0
    while True:
        newff = proc2(ff)
        if newff == ff:
            break
        """
        next_expected = next(source)
        if newff != next_expected:
            print("wrong")
            pprint(newff)
            print("correct")
            pprint(next_expected)
            print("prior")
            pprint(ff)
            pdb.set_trace()
            break

        if newff == ff:
            break
        """
        ccount = ccount + 1
        ff = newff
        if ccount > 1000000:
            break

    cc = Counter(concat(ff))
    assert cc["#"] == 2057

    return


testlines = [
    "L.LL.LL.LL",
    "LLLLLLL.LL",
    "L.L.L..L..",
    "LLLL.LL.LL",
    "L.LL.LL.LL",
    "L.LLLLL.LL",
    "..L.L.....",
    "LLLLLLLLLL",
    "L.LLLLLL.L",
    "L.LLLLL.LL",
]


tr1 = [
    "#.##.##.##",
    "#######.##",
    "#.#.#..#..",
    "####.##.##",
    "#.##.##.##",
    "#.#####.##",
    "..#.#.....",
    "##########",
    "#.######.#",
    "#.#####.##",
]

tr2 = [
    "#.LL.L#.##",
    "#LLLLLL.L#",
    "L.L.L..L..",
    "#LLL.LL.L#",
    "#.LL.LL.LL",
    "#.LLLL#.##",
    "..L.L.....",
    "#LLLLLLLL#",
    "#.LLLLLL.L",
    "#.#LLLL.##",
]

stable = [
    "#.#L.L#.##",
    "#LLL#LL.L#",
    "L.#.L..#..",
    "#L##.##.L#",
    "#.#L.LL.LL",
    "#.#L#L#.##",
    "..L.L.....",
    "#L#L##L#L#",
    "#.LLLLLL.L",
    "#.#L#L#.##",
]

r2res1 = [
    "#.##.##.##",
    "#######.##",
    "#.#.#..#..",
    "####.##.##",
    "#.##.##.##",
    "#.#####.##",
    "..#.#.....",
    "##########",
    "#.######.#",
    "#.#####.##",
]

r2res2 = [
    "#.LL.LL.L#",
    "#LLLLLL.LL",
    "L.L.L..L..",
    "LLLL.LL.LL",
    "L.LL.LL.LL",
    "L.LLLLL.LL",
    "..L.L.....",
    "LLLLLLLLL#",
    "#.LLLLLL.L",
    "#.LLLLL.L#",
]

if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer

    raw = Path("input-11.txt").read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    result = process(raw)
