from argparse import ArgumentParser
from datetime import datetime, timedelta
from functools import partial
from operator import methodcaller
from pathlib import Path
import json
import pdb
import requests
from colorama import Fore, Style
from requests_cache import CachedSession
from toolz import compose_left, do, identity
from tadhg_utils import (
    get_git_root,
    format_timedelta,
    from_8601,
    lconcat,
    lfilter,
    lmap,
    load_text,
    lpluck,
)

LEADBOARDS_URL_BASE = "https://adventofcode.com/2021/leaderboard/private/view/"

LEADERBOARDS = {
    "dash": "976765.json",
    "logan": "62916.json",
}

NAMES = {
    "Allan Shortlidge": "Allan",
    "Bryan Culbertson": "Bryan",
    "Dash": "Dash",
    "Stu": "stuglaser",
    "Tadhg O'Higgins": "Tadhg",
}

YEAR = "2022"

# OPENING_TIME = from_8601("2022-11-30 21:00")

opening_time = lambda: from_8601(f"{YEAR}-11-30 21:00")

testdata = """
{"members":{"869762":{"stars":0,"local_score":0,"global_score":0,"id":"869762","completion_day_level":{},
"name":"avanhatt","last_star_ts":"0"},
"818603":{"last_star_ts":1638855662,"completion_day_level":{"6":{"1":{"get_star_ts":1638770914},
"2":{"get_star_ts":1638771865}},
"1":{"1":{"get_star_ts":1638336652},
"2":{"get_star_ts":1638337371}},
"2":{"2":{"get_star_ts":1638422885},
"1":{"get_star_ts":1638422578}},
"7":{"1":{"get_star_ts":1638854991},
"2":{"get_star_ts":1638855662}},
"4":{"1":{"get_star_ts":1638596979},
"2":{"get_star_ts":1638597293}},
"3":{"2":{"get_star_ts":1638514663},
"1":{"get_star_ts":1638508778}},
"5":{"1":{"get_star_ts":1638683782},
"2":{"get_star_ts":1638685535}}},
"name":"stuglaser","id":"818603","stars":14,"global_score":0,"local_score":84},
"1160080":{"completion_day_level":{"5":{"2":{"get_star_ts":1638683498},
"1":{"get_star_ts":1638682633}},
"3":{"2":{"get_star_ts":1638515016},
"1":{"get_star_ts":1638513070}},
"4":{"1":{"get_star_ts":1638596021},
"2":{"get_star_ts":1638596477}},
"1":{"1":{"get_star_ts":1638335029},
"2":{"get_star_ts":1638335265}},
"7":{"1":{"get_star_ts":1638853692},
"2":{"get_star_ts":1638854070}},
"2":{"1":{"get_star_ts":1638421502},
"2":{"get_star_ts":1638421930}},
"6":{"2":{"get_star_ts":1638780986},
"1":{"get_star_ts":1638767236}}},
"name":"Tadhg O'Higgins","last_star_ts":1638854070,"id":"1160080","local_score":99,"stars":14,"global_score":0},
"864437":{"id":"864437","stars":0,"local_score":0,"global_score":0,"name":"Allan Shortlidge","completion_day_level":{},
"last_star_ts":"0"},
"1571995":{"stars":10,"local_score":56,"global_score":0,"id":"1571995","name":"Bryan Culbertson","completion_day_level":{"6":{"1":{"get_star_ts":1638860959},
"2":{"get_star_ts":1638861749}},
"2":{"2":{"get_star_ts":1638422719},
"1":{"get_star_ts":1638421603}},
"7":{"2":{"get_star_ts":1638855504},
"1":{"get_star_ts":1638854140}},
"1":{"2":{"get_star_ts":1638335736},
"1":{"get_star_ts":1638335541}},
"3":{"2":{"get_star_ts":1638860239},
"1":{"get_star_ts":1638853231}}},
"last_star_ts":1638861749},
"991403":{"name":"@pangburnout","completion_day_level":{},
"last_star_ts":"0","stars":0,"global_score":0,"local_score":0,"id":"991403"},
"976765":{"last_star_ts":1638853977,"name":"Dash","completion_day_level":{"6":{"1":{"get_star_ts":1638767070},
"2":{"get_star_ts":1638771999}},
"1":{"1":{"get_star_ts":1638335120},
"2":{"get_star_ts":1638335436}},
"2":{"2":{"get_star_ts":1638421504},
"1":{"get_star_ts":1638421393}},
"7":{"1":{"get_star_ts":1638853594},
"2":{"get_star_ts":1638853977}},
"5":{"2":{"get_star_ts":1638682647},
"1":{"get_star_ts":1638681325}},
"3":{"2":{"get_star_ts":1638509674},
"1":{"get_star_ts":1638508174}},
"4":{"1":{"get_star_ts":1638598047},
"2":{"get_star_ts":1638598901}}},
"id":"976765","stars":14,"local_score":105,"global_score":0},
"1181519":{"local_score":0,"stars":0,"global_score":0,"id":"1181519","name":"Chris F","completion_day_level":{},
"last_star_ts":"0"}},
"event":"2021","owner_id":"976765"}
"""


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
    parser.add_argument("id", type=str)
    parser.add_argument("--year", type=int, default=2021)
    options = parser.parse_args()
    leaderboard_id, year = options.id, options.year
    global YEAR
    YEAR = options.year
    # skip stuff for actaully getting the leaderboard here
    """
    if leaderboard_id
    url = f"https://adventofcode.com/{year}/leaderboard/private/view/{tail}"
        output = Path(f"input-{str(day).zfill(2)}.txt")
        cookies = dict([Path("../.session-cookie").read_text().strip().split("=")])
        res = requests.get(url, cookies=cookies)
        output.write_text(res.text.strip())
        print(res.text.strip())
    """
    # raw_json = testdata
    # data = json.loads(raw_json)
    data = get_data(leaderboard_id, year)
    process_data(data)


def get_data(leaderboard, year):
    lb_path = LEADERBOARDS.get(leaderboard, leaderboard)
    url = f"https://adventofcode.com/{year}/leaderboard/private/view/{lb_path}"
    cache_options = {"backend": "filesystem", "expire_after": 43200}
    session = CachedSession("../../site_cache", **cache_options)
    cookiepath = get_git_root() / "resources" / ".session-cookie"
    cookies = dict([load_text(cookiepath).strip().split("=")])
    response = session.get(url, cookies=cookies)
    if response.status_code != 200:
        pdb.set_trace()
    return response.json()


def rearrange_data(data):
    # We want to have an ordered bunch of rows, corresponding to each puzzle,
    # and each row should have the puzzle id and the list of people's times in
    # the same order as the intiial entries.
    # We can think about sorting it differently another time.
    entries = [data["members"][k] for k in data["members"]]
    ordered = sorted(entries, key=lambda x: -x["local_score"])
    names = lmap(lambda n: NAMES.get(n, n), lpluck("name", ordered))
    days = lmap(methodcaller("keys"), lpluck("completion_day_level", ordered))
    latest_day = max(map(int, lconcat(days)))
    puzzle_rows = []

    def get_timestamp(day, part, entry):
        times = entry["completion_day_level"]
        timestamp = (
            times.get(str(day), {}).get(str(part), {}).get("get_star_ts", 0)
        )
        return timestamp

    for i in range(1, 1 + latest_day):
        p1_info = []
        p2_info = []
        for entry in ordered:
            part_one_ts = get_timestamp(i, 1, entry)
            p1_info.append(part_one_ts)
            part_two_ts = get_timestamp(i, 2, entry)
            p2_info.append(part_two_ts)
        puzzle_rows.append(p1_info)
        puzzle_rows.append(p2_info)

    def check(idx_item):
        return sum([x[idx_item[0]] for x in puzzle_rows]) > 0

    filtered = lfilter(check, enumerate(names))
    filtered_cols = lpluck(0, filtered)
    filtered_names = lpluck(1, filtered)

    def filter_row(row):
        cols = lfilter(lambda i_r: i_r[0] in filtered_cols, enumerate(row))
        return lpluck(1, cols)

    filtered_rows = lmap(filter_row, puzzle_rows)

    def mark_winner(row):
        winner = min(filter(lambda x: x != 0, row))
        return [(item, item == winner) for item in row]

    with_winners = lmap(mark_winner, filtered_rows)

    return (filtered_names, with_winners)


def fmt_timestamps(day, timestamps):
    return [fmt_timestamp(day // 2, *timestamp) for timestamp in timestamps]


def fmt_timestamp(day, timestamp, win):
    start = opening_time() + timedelta(days=day)
    end = datetime.fromtimestamp(timestamp)
    delta = end - start
    if delta.days < 0:
        return ("—", False)
    return (format_timedelta(delta), win)


def rjust_row(width, row):
    justify = methodcaller("rjust", width)
    brighten = lambda s: f"{Fore.CYAN}{s}{Style.RESET_ALL}"
    make_cell = lambda c: brighten(justify(c[0])) if c[1] else justify(c[0])
    if len(row[0]) == 2 and row[0][1] in (True, False):
        return lmap(make_cell, row)
    return [justify(str(col)) for col in row]


def process_data(data):
    names, rows = rearrange_data(data)
    longest_name = max([*map(len, names)] + [11])
    # print_names = [name.rjust(longest_name) for name in names]
    print_names = rjust_row(longest_name, names)
    headers = "        ".join(["Puzzle"] + print_names)
    hr = "".join(["-" * len(headers)])
    times = lmap(lambda _: fmt_timestamps(*_), enumerate(rows))
    # pdb.set_trace()
    print_times = [rjust_row(longest_name, row) for row in times]

    def add_puzzle(day, times):
        base_day = str(day // 2 + 1)
        puzzle = "1" if day % 2 == 0 else "2"
        return [f"{base_day}.{puzzle}".rjust(6)] + times

    print_rows = [add_puzzle(i, row) for i, row in enumerate(print_times)]

    print(headers)
    print(hr)
    for i, row in enumerate(print_rows):
        if i != 0 and i % 10 == 0:
            print(hr)
            print(headers)
            print(hr)
        print("        ".join(row))


if __name__ == "__main__":
    cli_main()
