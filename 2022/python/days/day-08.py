from itertools import takewhile

from toolz import pipe

from tadhg_utils import (
    lmap,  # A version of map that returns a list.
    splitstriplines,
)


TEST_ANSWERS = (21, 8)
PUZZLE_ANSWERS = (1705, 371200)


def preprocess(data):
    procs = [
        splitstriplines,
    ]
    result = pipe(data, *procs)
    return result


def part_one(data):
    visible = 0
    for i, line in enumerate(data):
        for j in range(len(line)):
            if (
                i == 0
                or j == 0
                or i == (len(line) - 1)
                or j == (len(data) - 1)
            ):
                visible = visible + 1
            else:
                height = int(data[i][j])
                line = lmap(int, data[i])
                if all(x < height for x in line[:j]) or all(
                    y < height for y in line[j + 1 :]
                ):
                    visible = visible + 1
                    continue
                col = lmap(int, [data[ln][j] for ln in range(len(data))])
                if all(a < height for a in col[:i]) or all(
                    b < height for b in col[i + 1 :]
                ):
                    visible = visible + 1

    return visible


def part_two(data):
    scores = []
    for i, line in enumerate(data):
        for j in range(len(line)):
            if (
                i == 0
                or j == 0
                or i == (len(line) - 1)
                or j == (len(data) - 1)
            ):
                pass
            else:
                height = int(data[i][j])
                line = lmap(int, data[i])
                to_west = line[:j][::-1]
                vdwest = len(list(takewhile(lambda x: x < height, to_west)))
                if vdwest != len(to_west):  # we count a blocking tree
                    vdwest = vdwest + 1
                to_east = line[j + 1 :]
                vdeast = len(list(takewhile(lambda x: x < height, to_east)))
                if vdeast != len(to_east):  # we count a blocking tree
                    vdeast = vdeast + 1
                col = lmap(int, [data[ln][j] for ln in range(len(data))])
                to_north = col[:i][::-1]
                vdnorth = len(list(takewhile(lambda x: x < height, to_north)))
                if vdnorth != len(to_north):  # we count a blocking tree
                    vdnorth = vdnorth + 1
                to_south = col[i + 1 :]
                vdsouth = len(list(takewhile(lambda x: x < height, to_south)))
                if vdsouth != len(to_south):  # we count a blocking tree
                    vdsouth = vdsouth + 1
                scores = scores + [vdwest * vdeast * vdnorth * vdsouth]
    return max(scores)
