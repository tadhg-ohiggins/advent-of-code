from argparse import ArgumentParser
from functools import partial
from operator import methodcaller
from pathlib import Path
import requests
from toolz import compose_left, do, identity


def cli_main():
    """
    Silliness: how do get the day from a series of functions

    add_arg = methodcaller("add_argument", "day", type=int)
    do_add_arg = partial(do, add_arg)
    parse_args = methodcaller("parse_args")
    get_day = partial(lambda o, s: getattr(s, o), "day")
    day = compose_left(ArgumentParser, do_add_arg, parse_args, get_day)()
    import pdb

    pdb.set_trace()
    """
    parser = ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("--year", type=int, default=2022)
    options = parser.parse_args()
    day, year = options.day, options.year
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    output = Path(f"input-{str(day).zfill(2)}.txt")
    cookies = dict([Path("../.session-cookie").read_text().strip().split("=")])
    res = requests.get(url, cookies=cookies)
    output.write_text(res.text.strip())
    print(res.text.strip())


if __name__ == "__main__":
    cli_main()
