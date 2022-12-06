#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
from itertools import product
import unittest
import re
import sys

import numpy as np


INPUT = "input-17.txt"


def zeros(*args, **kwargs):
    return np.zeros(*args, **kwargs, dtype=np.int32)


def arr_contains(arr, idx):
    for n in range(arr.ndim):
        if not (0 <= idx[n] < arr.shape[n]):
            return False
    return True


def main():
    with open(INPUT, "r") as fin:
        lines = [line.rstrip() for line in fin]

    # Puts into an array
    world = set()
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                world.add((0, 0, i, j))

    print("START")
    print(world)

    # offsets = orthodiag_offsets(4)

    import datetime

    ps = datetime.datetime.now()
    for iteration in range(6):
        print("\n\n===== ", iteration)
        next_world = set()
        ncnt = {}  # pt: count

        for pt in world:
            for neighbor in product(
                (pt[0] - 1, pt[0], pt[0] + 1),
                (pt[1] - 1, pt[1], pt[1] + 1),
                (pt[2] - 1, pt[2], pt[2] + 1),
                (pt[3] - 1, pt[3], pt[3] + 1),
            ):
                if neighbor == pt:
                    pass
                else:
                    ncnt[neighbor] = 1 + ncnt.get(neighbor, 0)

        for pt in world:
            if ncnt.get(pt, 0) in (2, 3):
                next_world.add(pt)
        for pt, n in ncnt.items():
            if n == 3:
                next_world.add(pt)

        world = next_world
        print("Ater", iteration + 1, "cycles:", len(world))
        # print(world)

    pe = datetime.datetime.now()
    print(pe - ps)
    print("part x:", len(world))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
