import importlib
from tutils import (
    load_and_process_input,
    run_tests,
)


DAY = "02"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
MODULE = f"improved-day-{DAY}"
TA1 = 15
TA2 = 12
ANSWER1 = 13268
ANSWER2 = 15508

day = importlib.import_module(f".{MODULE}", "days")
preprocess, part_one, part_two = day.preprocess, day.part_one, day.part_two


def cli_main() -> None:
    data = load_and_process_input(INPUT, [preprocess])
    run_tests(TEST, TA1, TA2, ANSWER1, [preprocess], part_one, part_two)
    answer_one = part_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = part_two(data)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
