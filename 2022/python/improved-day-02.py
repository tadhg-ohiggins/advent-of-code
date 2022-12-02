from functools import partial
from toolz import pipe
from toolz.curried import identity, map as cmap
from tutils import (
    innermap,
    lfilter,
    lmap,
    load_and_process_input,
    run_tests,
    splitstriplines,
)

DAY = "02"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 15
TA2 = 12
ANSWER1 = 13268
ANSWER2 = 15508

invertd = lambda d: {v: k for k, v in d.items()}

TOSHAPE = {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "R",
    "Y": "P",
    "Z": "S",
}
TOCHAR = invertd(TOSHAPE)

BEATS = {
    "R": "S",
    "P": "R",
    "S": "P",
}
LOSES = invertd(BEATS)


def get_result(pair):
    shapes = lmap(TOSHAPE.get, pair)
    if shapes[0] == shapes[1]:
        return 3
    if BEATS.get(shapes[1]) == shapes[0]:
        return 6
    return 0


def shape_score(move):
    return list(BEATS.keys()).index(TOSHAPE.get(move)) + 1


def get_moves(pair):
    transforms = {"X": BEATS.get, "Y": identity, "Z": LOSES.get}
    funcs = (TOSHAPE.get, transforms[pair[1]], TOCHAR.get)
    return [pair[0], pipe(pair[0], *funcs)]


def get_score(pair):
    return get_result(pair) + shape_score(pair[1])


def process_one(data):
    procs = [cmap(get_score), sum]
    result = pipe(data, *procs)
    return result


def process_two(data):
    procs = [cmap(get_moves), cmap(get_score), sum]
    result = pipe(data, *procs)
    return result


def cli_main() -> None:
    input_funcs = [splitstriplines, partial(lmap, str.split)]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process_two(data)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
