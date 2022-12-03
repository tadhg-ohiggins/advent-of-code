from functools import partial
from toolz import pipe
from toolz.curried import map as cmap
from tutils import (
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


def process_one(data):
    return pipe(data, *(cmap(get_result), sum))


def process_two(data):
    return pipe(data, *(cmap(get_moves), cmap(get_result), sum))


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
