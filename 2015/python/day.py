import argparse
import importlib
import richxerox
from tutils import (
    load_and_process_input,
    run_tests,
)

"""
python day.py [day] [optional: "o"(default)/"i"/"b"]

Looks in the days/ subdirectory for day-[day].py and imports from it the
functions:

+   preprocess
+   part_one
+   part_two

It also imports these tuples containing test and puzzle answers:

+   TEST_ANSWERS
+   PUZZLE_ANSWERS

It looks in the data/ subdirectory for input-[day].txt and test-input-[day].txt
and handles loading their contents, running test and puzzle answers, and
printing answers; it also copies the latest answer to the MacOS clipboard.

The default for the optional script arg does the above. Values for this can
start with:

+   "o" for the original first-pass script (the default).
+   "i" for an improved version, which will cause the script to look in days/
    for improved-day-[day].py.
+   "b" for both.
"""


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
