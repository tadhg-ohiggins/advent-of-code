from argparse import ArgumentParser
import datetime
from functools import reduce
from operator import add
from bs4 import BeautifulSoup  # type: ignore
import requests
from rich.console import Console
from rich.markdown import Markdown
from tadhg_utils import (
    get_git_root,
    lmap,
    load_text,
    run_process,
)


def cli_main():
    """
    python submit.py [answer] --day [day] --year [year] --part [part]
    """
    options = parse_args()
    if options.day is None:
        aocdate = datetime.datetime.now() + datetime.timedelta(hours=3)
        options.day = aocdate.day
    url = f"https://adventofcode.com/{options.year}/day/{options.day}/answer"
    cookiepath = get_git_root() / "resources" / ".session-cookie"
    cookies = dict([load_text(cookiepath).strip().split("=")])
    payload = {"level": options.part, "answer": options.answer}
    res = requests.post(url, data=payload, cookies=cookies)
    html = BeautifulSoup(res.text, "html.parser")
    print_response(html)


def print_response(html):
    articles = lmap(str, html.select("article"))
    content = reduce(add, articles, "")
    simplify = [
        "python",
        "/Users/tadhg/vcs/rest_tools_private/python/simplify_html.py",
    ]
    stext = run_process(simplify, {"input": content}).stdout
    pandoc = ["pandoc", "-f", "html", "-t", "gfm"]
    ptext = run_process(pandoc, {"input": stext}).stdout
    console = Console()
    md = Markdown(ptext)
    console.print(md)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("answer")
    parser.add_argument("--day", type=int, default=None)
    parser.add_argument("--year", type=int, default=2022)
    parser.add_argument("--part", type=int, default=1)
    return parser.parse_args()


if __name__ == "__main__":
    cli_main()
