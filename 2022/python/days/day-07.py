from functools import partial, reduce
from pathlib import Path

from toolz import pipe

from tutils import trace, splitblocks
from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    lfilter,
    lmap,  # A version of map that returns a list.
    splitstriplines,
    splitstrip,
    star,
)
import pdb


TEST_ANSWERS = (95437, 24933642)
PUZZLE_ANSWERS = (1915606, None)


def all_diff(seq):
    return len(seq) == len(set(seq))


def preprocess(data):
    # first thing I think we need here is distinction between commands and
    # output.
    # All lines that don't start with $ are output for last line that started
    # with $.
    procs = [
        str.strip,
        partial(splitstrip, sep="$"),
        cmap(splitstriplines),
    ]
    result = pipe(data, *procs)
    return result


def interpret_cmd(fs: dict, cmd: list[str]):
    if cmd[0].startswith("cd "):
        targ = cmd[0][3:].strip()
        if targ == "/":
            fs["_current"] = Path("/")
        elif targ == "..":
            fs["_current"] = Path(fs["_current"]).parent
        else:
            fs["_current"] = Path(fs["_current"]) / targ
        if Path(fs["_current"]) not in fs:
            fs[Path(fs["_current"])] = {"_subdirs": [], "_files": []}
    elif cmd[0].startswith("ls"):
        output = cmd[1:]
        subdirs_strs = [e for e in output if e.startswith("dir")]
        for sd in subdirs_strs:
            fs[Path(fs["_current"])]["_subdirs"].append(sd.split(" ")[1])
        files_strs = [e for e in output if not e.startswith("dir")]
        for fd in files_strs:
            size, fname = fd.split(" ", 1)
            fs[Path(fs["_current"])]["_files"].append((int(size), fname))

    return fs


def calc_size(fs, path, size):
    if len(fs[path]["_files"]):
        size = size + sum([f[0] for f in fs[path]["_files"]])
    if len(fs[path]["_subdirs"]):
        for sd in fs[path]["_subdirs"]:
            size = calc_size(fs, path / sd, size)
    # The following line doesn't actually work because it accumulates more than
    # it should; it's still accurate in terms of what's returned by the
    # function when given a specific subdirectory, but some of the _size values
    # of its subdirectories will not be accurate.
    fs[path]["_size"] = size
    return size


def part_one(data):
    fs = {Path("/"): {"_subdirs": [], "_files": []}, "_current": Path("/")}
    fs = reduce(lambda acc, c: interpret_cmd(acc, c), data, fs)
    # size = calc_size(fs, Path("/"), 0)
    # sized = calc_size(fs, Path("/d"), 0)
    dirs = [p for p in fs.keys() if isinstance(p, Path)]
    under100k = sum(
        [fs[p]["_size"] for p in dirs if calc_size(fs, p, 0) < 100000]
    )
    return under100k


def part_two(data):
    fs = {Path("/"): {"_subdirs": [], "_files": []}, "_current": Path("/")}
    fs = reduce(lambda acc, c: interpret_cmd(acc, c), data, fs)
    size = calc_size(fs, Path("/"), 0)
    dirs = [p for p in fs.keys() if isinstance(p, Path)]
    totalsize = 70000000
    curfree = totalsize - size
    targetfree = 30000000
    difftofree = targetfree - curfree
    candidate = min(
        [fs[p]["_size"] for p in dirs if calc_size(fs, p, 0) > difftofree]
    )
    return candidate
