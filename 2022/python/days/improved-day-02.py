from toolz import pipe
from toolz.curried import map as cmap
from tutils import splitstriplines

TEST_ANSWERS = (15, 12)
PUZZLE_ANSWERS = (13268, 15508)

# The ordering here determines much of the list-shifting and modulo math below:
BEATS = {
    "A": "Y",
    "B": "Z",
    "C": "X",
}
OPP = list(BEATS.keys())
MINE = list(BEATS.values())


def get_result(pair):
    shape_score = (MINE[2:] + MINE[:2]).index(pair[1]) + 1
    distance = (OPP.index(pair[0]) - MINE.index(pair[1])) % 3
    return shape_score + 6 - (distance * 3)


def get_moves(pair):
    amount = {"X": 1, "Y": 2, "Z": 0}.get(pair[1])
    response = MINE[(OPP.index(pair[0]) + amount) % 3]
    return [pair[0], response]


def preprocess(data):
    return pipe(data, *(splitstriplines, cmap(str.split), list))


def part_one(data):
    return pipe(data, *(cmap(get_result), sum))


def part_two(data):
    return pipe(data, *(cmap(get_moves), cmap(get_result), sum))
