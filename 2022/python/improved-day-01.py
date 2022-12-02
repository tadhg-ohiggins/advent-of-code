from functools import partial
from toolz import pipe
from toolz.curried import get, map as cmap
from tutils import (
    innermap,
    load_and_process_input,
    run_tests,
    splitblocks,
    splitstriplines,
)

DAY = "01"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 24000
TA2 = 45000
ANSWER1 = 69206
ANSWER2 = 197400


def process_one(data):
    return pipe(data, *(cmap(sum), sorted))[-1]


def process_two(data):
    return pipe(data, *(cmap(sum), sorted, get([-1, -2, -3]), sum))


def cli_main() -> None:
    input_funcs = [
        splitblocks,
        cmap(splitstriplines),
        partial(innermap, int),
    ]
    data = load_and_process_input(INPUT, input_funcs)
    answer_one = process_one(data)
    # print(answer_one)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process_two(data)
    print(answer_two)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
