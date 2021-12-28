from collections import Counter
from functools import cache, partial, reduce
from math import prod
import pdb
import aoc
import networkx as nx
from toolz import keyfilter, sliding_window

from aoc import Point, adjacent_transforms, generate_bounded_coords
from tadhg_utils import (
    lcompact,
    lconcat,
    lfilter,
    lmap,
    splitstrip,
    splitstriplines,
)


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 1588
TA2 = 2188189693529
A1 = 2657
A2 = None


def parse_data(data):
    start, raw_rules = data.split("\n\n")
    rules = lmap(lambda x: splitstrip(x, sep="->"), splitstriplines(raw_rules))
    rules = dict(rules)

    return start, rules


def process_step(curr, rules):
    pairs = lmap("".join, sliding_window(2, curr))

    def alter_pair(pair):
        if pair in rules:
            pair = pair[0] + rules[pair] + pair[1]
        return pair

    def merge(couplets):
        st = ""
        for i, couplet in enumerate(couplets):
            if not st:
                st = couplet
            else:
                st = st[: 2 * (i)] + couplet
        return st

    xx = merge(lmap(alter_pair, pairs))
    xx2 = merge(xx[0])
    return xx2, rules


def make_quads(term):
    s, e = 0, 4
    refs = []
    while e <= len(term):
        refs.append((s, e))
        s = s + 3
        e = e + 3
    return [term[s:e] for s, e in refs]


@cache
def make_quads2(quarter, term):
    s, e, i = 0, quarter, 0
    refs = []

    while len(refs) < 4:
        refs.append((s, e))
        s = s + quarter - i
        e = e + quarter - i
        i = i + 1
    return [term[s:e] for s, e in refs]


def naive_step(curr, rules):
    @cache
    def naive_step_inner(curr):
        @cache
        def alter_pair(pair):
            return pair[0] + rules[pair] + pair[1]

        pairs = tuple(lmap("".join, sliding_window(2, curr)))
        return do_merge(tuple(lmap(alter_pair, pairs)))

    return naive_step_inner(curr)


def naive_steps(curr, rules, num):
    for i in range(num):
        curr = naive_step(curr, rules)
        print(i)
    return curr


def process_one(data):
    start, rules = data
    curr = start

    def better_step(curr):
        def merge(couplets):
            st = ""
            for i, couplet in enumerate(couplets):
                if not st:
                    st = couplet
                else:
                    st = st[: 2 * (i)] + couplet
            return st

        def alter_pair(pair):
            if pair in rules:
                pair = pair[0] + rules[pair] + pair[1]
            return pair

        @cache
        def alter_quad(quad):
            pairs = lmap("".join, sliding_window(2, quad))
            return merge(lmap(alter_pair, pairs))

        quads = make_quads(curr)
        altered_quads = map(alter_quad, quads)
        stuff = ""
        for q in altered_quads:
            stuff = stuff[:-1] + q

        return stuff

    for i in range(10):
        prev_length = 3 * (2 ** (i - 1)) + 1
        p1, p2 = prev_length, prev_length - 1
        if prev_length > 7:
            curr = better_step(curr[:p1]) + better_step(curr[p2:])[1:]
        else:
            curr = better_step(curr)
    counted = Counter(curr)
    return counted.most_common()[0][1] - counted.most_common()[-1][1]


def do_merge(segments):
    stuff = ""
    for segment in segments:
        if not stuff:
            stuff = segment
        else:
            stuff = stuff + segment[1:]
    return stuff


def process_two(data):
    start, rules = data
    num = 5
    curr = naive_steps(start, rules, num)
    curr2 = naive_steps(start, rules, 2)
    naive2 = naive_steps(start, rules, 2)
    nn2, nc2, cb2 = [naive_steps(x, rules, 2) for x in ["NN", "NC", "CB"]]
    chec2 = curr2 == do_merge((nn2, nc2, cb2))
    curr3 = naive_steps(start, rules, 3)
    nn3, nc3, cb3 = [naive_steps(x, rules, 3) for x in ["NN", "NC", "CB"]]
    chec3 = curr3 == do_merge((nn3, nc3, cb3))
    curr4 = naive_steps(start, rules, 4)
    nn4, nc4, cb4 = [naive_steps(x, rules, 4) for x in ["NN", "NC", "CB"]]
    chec4 = curr4 == do_merge((nn4, nc4, cb4))
    twos = {rule: naive_steps(rule, rules, 2) for rule in rules}
    ones = {rule: naive_steps(rule, rules, 1) for rule in rules}
    innc3 = [x for x in twos.values() if x in nc3]
    inc3 = [(x, v) for x, v in twos.items() if v in curr3]
    nn = naive_steps("NN", rules, num)
    nc = naive_steps("NC", rules, num)
    cb = naive_steps("CB", rules, num)
    """
    xx = [do_steps("BN", rules, i) for i in range(num - 1)]
    stripped = (
        curr.replace(nn, nn[-1]).replace(nc, "|" + nc[-1]).replace(cb, cb[-1])
    )
    matches = lfilter(
        lambda x: curr[25:32] in x,
        [do_steps("BN", rules, i) for i in range(num - 1)],
    )
    """
    """
    xcurr = do_steps(start, rules, 10)
    xstuff = ""
    for k in xcurr:
        xstuff = xstuff + k * xcurr[k]

    """
    pdb.set_trace()
    nn40 = naive_steps("NN", rules, 40)
    return counted.most_common()[0][1] - counted.most_common()[-1][1]


def xdo_steps(curr, rules, num):
    pairs = lmap("".join, sliding_window(2, curr))
    couplets = {p: 1 for p in pairs}
    for i in range(num):
        print(i, couplets, sum(couplets.values()))
        new_couplets = {}
        for couplet in couplets:
            triplet = couplet[0] + rules[couplet] + couplet[1]
            newpairs = lmap("".join, sliding_window(2, triplet))
            for np in newpairs:
                if np in new_couplets:
                    new_couplets[np] = new_couplets[np] + 1
                else:
                    new_couplets[np] = 1
        for k in couplets:
            if k in new_couplets:
                new_couplets[k] = new_couplets[k] * couplets[k]
        couplets = new_couplets
    return couplets


def do_steps(curr, rules, num):
    sequences = {}

    def merge(couplets):
        st = ""
        for i, couplet in enumerate(couplets):
            if not st:
                st = couplet
            else:
                st = st[: 2 * (i)] + couplet
        return st

    @cache
    def alter_pair(pair):
        if pair in rules:
            pair = pair[0] + rules[pair] + pair[1]
        return pair

    for pair in rules:
        sequences[pair] = alter_pair(pair)

    @cache
    def alter_quad(quad):
        pairs = lmap("".join, sliding_window(2, quad))
        return merge(lmap(alter_pair, pairs))

    @cache
    def better_step(curr):
        print(len(sequences))

        if curr in sequences:
            return sequences[curr]
        elif len(curr) > 7:
            quads = make_quads(curr)
            altered_quads = map(alter_quad, quads)
            stuff = ""
            for q in altered_quads:
                stuff = stuff[:-1] + q

            if curr not in sequences:
                sequences[curr] = stuff

            return stuff
        else:
            pairs = lmap("".join, sliding_window(2, curr))
            return merge(lmap(alter_pair, pairs))

    for i in range(num):
        curr = better_step(curr)
        print("len:", len(curr))
        """
        prev_length = 3 * (2 ** (i - 2)) + 1
        print(i, len(curr), prev_length)

        p1, p2 = prev_length, prev_length - 1
        if False:
            # if any(seq in curr for seq in sequences):
            for seq in sequences:
                if curr.startswith(seq):
                    curr = curr.replace(seq, sequences[seq])
                else:
                    curr = curr.replace(seq, sequences[seq][1:])

        else:
            if i > 3:
                qs = make_quads2(prev_length, curr)
                curr = (
                    better_step(qs[0])
                    + better_step(qs[1])[1:]
                    + better_step(qs[2])[1:]
                    + better_step(qs[3])[1:]
                )
            else:
                oldcurr = curr
                curr = better_step(curr)
                if oldcurr not in sequences:
                    sequences[oldcurr] = curr
        """

        """
        for seq in sorted(sequences.keys(), key=lambda x: -len(x))
            curr = 
            if seq in curr:
                p1 = curr.index(seq)
                p2 = p1 + len(seq)
                curr = (
                    better_step(curr[:p1])
                    + sequences[seq][1:]
                    + better_step(curr[p2:])
                )
                in_seq = True

        if not in_seq:
            if i > 3:
                qs = make_quads2(prev_length, curr)
                curr = (
                    better_step(qs[0])
                    + better_step(qs[1])[1:]
                    + better_step(qs[2])[1:]
                    + better_step(qs[3])[1:]
                )
            else:
                curr = better_step(curr)

        if i > 3:
            qs = make_quads2(prev_length, curr)
            curr = (
                better_step(qs[0])
                + better_step(qs[1])[1:]
                + better_step(qs[2])[1:]
                + better_step(qs[3])[1:]
            )
        else:
            curr = better_step(curr)
        """
        """
        prev_length = 3 * (2 ** (i - 1)) + 1
        print(i, len(curr), prev_length)

        p1, p2 = prev_length, prev_length - 1
        if prev_length > 7:
            curr = better_step(curr[:p1]) + better_step(curr[p2:])[1:]
        else:
            curr = better_step(curr)
        """
        print(Counter(curr))

    return curr


def cli_main() -> None:
    input_funcs = [parse_data]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    # result_one = process_one(data)
    # print(result_one)
    # result_two = process_two(data)
    # aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
"""
--- Day 13: Transparent Origami ---

You reach another volcanically active part of the cave. It would be nice if you
could do some kind of thermal imaging so you could tell ahead of time which
caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you
activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.

Apparently, the Elves have never used this feature. To your surprise, you
manage to find the manual; as you go to open it, page 1 falls out. It's a large
sheet of transparent paper! The transparent paper is marked with random dots
and includes instructions on how to fold it up (your puzzle input). For
example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

The first section is a list of dots on the transparent paper. 0,0 represents
the top-left coordinate. The first value, x, increases to the right. The second
value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0,
and the coordinate 0,7 is below 0,0. The coordinates in this example form the
following pattern, where # is a dot on the paper and . is an empty, unmarked
position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Then, there is a list of fold instructions. Each instruction indicates a line
on the transparent paper and wants you to fold the paper up (for horizontal
y=... lines) or left (for vertical x=... lines). In this example, the first
fold instruction is fold along y=7, which designates the line formed by all of
the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Because this is a horizontal line, fold the bottom half up. Some of the dots
might end up overlapping after the fold is complete, but dots will never appear
exactly on a fold line. The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........

Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the
transparent paper is folded; after the fold is complete, those dots appear in
the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot
just below them in the result (at 0,3) remains visible, as it can be seen
through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge
together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....

Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....

The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the
first fold. After the first fold in the example above, 17 dots are visible -
dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on
your transparent paper?

Your puzzle answer was 631.

--- Part Two ---

Finish folding the transparent paper according to the instructions. The manual
says the code is always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?

Your puzzle answer was EFLFJGRF.
"""
