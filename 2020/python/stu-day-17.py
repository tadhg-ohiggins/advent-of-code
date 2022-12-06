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

# from utils import *

INPUT = "input-17.txt"
# INPUT='TEMP'


def pad_array(arr):
    import numpy as np

    # Should we pad the bottom/top of the array?
    pad_lo = [False for _ in arr.shape]
    pad_hi = [False for _ in arr.shape]
    for n in range(arr.ndim):
        lo_slice = tuple(0 if i == n else None for i in range(arr.ndim))
        pad_lo[n] = np.sum(arr[lo_slice]) > 0

        hi_slice = tuple(-1 if i == n else None for i in range(arr.ndim))
        pad_hi[n] = np.sum(arr[hi_slice]) > 0

    output_shape = [
        arr.shape[n] + pad_lo[n] + pad_hi[n] for n in range(arr.ndim)
    ]
    output = np.zeros(output_shape, dtype=arr.dtype)

    # Where to place the input inside the output
    set_rect = [
        slice(int(pad_lo[n]), -1 if pad_hi[n] else None)
        for n in range(arr.ndim)
    ]
    output[tuple(set_rect)] = arr
    return output


def zeros(*args, **kwargs):
    return np.zeros(*args, **kwargs, dtype=np.int32)


def arr_contains(arr, idx):
    for n in range(arr.ndim):
        if not (0 <= idx[n] < arr.shape[n]):
            return False
    return True


# Offsets to neighbors. In 2d, these are 8-neighbors
def orthodiag_offsets(rank):
    offsets = np.zeros((3 ** rank - 1, rank), dtype=np.int32)
    i = 0
    for off in product(*[(-1, 0, 1) for _ in range(rank)]):
        if not all(x == 0 for x in off):
            offsets[i] = off
            i += 1
    return offsets


def main():
    with open(INPUT, "r") as fin:
        lines = [line.rstrip() for line in fin]

    # Puts into an array
    world = np.zeros([1, 1, len(lines), len(lines[0])], dtype=np.int32)
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            world[0][0][i][j] = 1 if lines[i][j] == "#" else 0

    print("START")
    print(world)

    # offsets = orthodiag_offsets(4)

    for iteration in range(6):
        print("\n\n===== ", iteration)
        world = pad_array(world)

        next_world = world.copy()
        for i, j, k, l in product(*[range(n) for n in world.shape]):
            # Neighbors
            ncnt = (
                np.sum(
                    world[
                        max(i - 1, 0) : i + 2,
                        max(j - 1, 0) : j + 2,
                        max(k - 1, 0) : k + 2,
                        max(l - 1, 0) : l + 2,
                    ]
                )
                - world[i, j, k, l]
            )

            if world[i, j, k, l]:
                if not (ncnt == 2 or ncnt == 3):
                    next_world[i, j, k, l] = 0
            else:
                if ncnt == 3:
                    next_world[i, j, k, l] = 1

        world = next_world
        print("Ater", iteration + 1, "cycle:", np.sum(world))
        # print(world)

    print("part x:", np.sum(world))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
