from argparse import ArgumentParser
import datetime
from functools import reduce
from operator import add
from pathlib import Path
from bs4 import BeautifulSoup  # type: ignore
import requests
from tadhg_utils import (
    get_git_root,
    lmap,
    load_text,
    run_process,
)


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
    parser.add_argument("--day", type=int, default=None)
    parser.add_argument("--year", type=int, default=2022)
    options = parser.parse_args()
    if options.day is None:
        aocdate = datetime.datetime.now() + datetime.timedelta(hours=3)
        options.day = aocdate.day
    day, year = options.day, options.year
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookiepath = get_git_root() / "resources" / ".session-cookie"
    cookies = dict([load_text(cookiepath).strip().split("=")])
    res = requests.get(url, cookies=cookies)
    if Path("./data/").exists() and Path("./data/").is_dir():
        data_output = Path("./data") / Path(f"input-{str(day).zfill(2)}.txt")
        data_output.write_text(res.text.strip(), encoding="utf-8")
    else:
        output = Path(f"input-{str(day).zfill(2)}.txt")
        output.write_text(res.text.strip(), encoding="utf-8")

    purl = f"https://adventofcode.com/{year}/day/{day}"
    tres = requests.get(purl, cookies=cookies)
    html = BeautifulSoup(tres.text, "html.parser")
    articles = lmap(str, html.select("article"))
    content = reduce(add, articles, "")
    simplify = [
        "python",
        "/Users/tadhg/vcs/rest_tools_private/python/simplify_html.py",
    ]
    stext = run_process(simplify, {"input": content}).stdout
    pandoc = ["pandoc", "-f", "html", "-t", "gfm"]
    ptext = run_process(pandoc, {"input": stext}).stdout

    if Path("./data/").exists() and Path("./data/").is_dir():
        puzzle = Path("./data") / Path(f"puzzle-{str(day).zfill(2)}.md")
    else:
        puzzle = Path(f"puzzle-{str(day).zfill(2)}.md")
    puzzle.write_text(ptext.strip(), encoding="utf-8")

    # print(res.text.strip())


if __name__ == "__main__":
    cli_main()
