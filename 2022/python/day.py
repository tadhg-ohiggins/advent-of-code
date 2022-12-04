import argparse
import importlib
import richxerox
from tutils import (
    load_and_process_input,
    run_tests,
)


def setup_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=lambda s: s.zfill(2))
    parser.add_argument("scripts", type=str, nargs="?", default="original")
    return parser


def run_day(daynum, improved=False):
    imprstr = "improved-" if improved else ""
    module = f"{imprstr}day-{daynum}"
    day = importlib.import_module(f".{module}", "days")
    puzzle, test = f"data/input-{daynum}.txt", f"data/test-input-{daynum}.txt"
    data = load_and_process_input(puzzle, [day.preprocess])
    run_tests(
        test,
        day.TEST_ANSWERS[0],
        day.TEST_ANSWERS[1],
        day.PUZZLE_ANSWERS[0],
        [day.preprocess],
        day.part_one,
        day.part_two,
    )
    answer_one = day.part_one(data)
    print("Answer one:", answer_one)
    richxerox.copy(str(answer_one))
    if day.PUZZLE_ANSWERS[0] is not None:
        assert answer_one == day.PUZZLE_ANSWERS[0]
    answer_two = day.part_two(data)
    if answer_two:
        print("Answer two:", answer_two)
        richxerox.copy(str(answer_two))
        if day.PUZZLE_ANSWERS[1] is not None:
            assert answer_two == day.PUZZLE_ANSWERS[1]


def cli_main(args: [list | None] = None) -> None:
    options = setup_cli_parser().parse_args(args)
    if options.scripts.startswith("b"):
        print("First-pass version:")
        print("")
        run_day(options.day)
        print("")
        print("Cleaned-up version:")
        print("")
        run_day(options.day, improved=True)
    elif options.scripts.startswith("i"):
        print("Cleaned-up version:")
        print("")
        run_day(options.day, improved=True)
    else:
        print("First-pass version:")
        print("")
        run_day(options.day)


if __name__ == "__main__":
    cli_main()
