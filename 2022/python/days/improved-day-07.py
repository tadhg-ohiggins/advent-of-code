from functools import partial, reduce
from pathlib import Path

from toolz import pipe

from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    groupby_into_dict,
    splitstriplines,
    splitstrip,
)


TEST_ANSWERS = (95437, 24933642)
PUZZLE_ANSWERS = (1915606, 5025657)


def get_initial():
    return {Path("/"): {"_subdirs": [], "_files": []}, "_current": Path("/")}


def interpret_cmd(fs: dict, cmd: list[str]):
    # Mutates fs in place…
    if cmd[0].startswith("cd"):
        fs["_current"] = Path(fs["_current"], cmd[0][3:].strip()).resolve()
        if fs["_current"] not in fs:
            fs[fs["_current"]] = {"_subdirs": [], "_files": []}
    elif cmd[0].startswith("ls"):
        grouped = groupby_into_dict(lambda x: x.startswith("dir"), cmd[1:])
        cur = fs[fs["_current"]]
        dirs, files = grouped.get(True, []), grouped.get(False, [])
        cur["_subdirs"] = cur["_subdirs"] + [d.split(" ")[1] for d in dirs]
        for fd in files:
            size, fname = fd.split(" ", 1)
            cur["_files"].append((int(size), fname))

    return fs


def calc_size(fs, path, size):
    filesize, subdirsize = 0, 0
    if len(fs[path]["_files"]):
        filesize = sum([f[0] for f in fs[path]["_files"]])

    if len(fs[path]["_subdirs"]):
        for sd in fs[path]["_subdirs"]:
            subdirsize += calc_size(fs, path / sd, 0)
    return size + filesize + subdirsize


def get_dir_sizes(fs):
    dirs = [p for p in fs.keys() if isinstance(p, Path)]
    return (calc_size(fs, d, 0) for d in dirs)


def preprocess(data):
    procs = (
        str.strip,
        partial(splitstrip, sep="$"),
        cmap(splitstriplines),
    )
    return pipe(data, *procs)


def part_one(data):
    fs = reduce(lambda acc, c: interpret_cmd(acc, c), data, get_initial())
    sizes = get_dir_sizes(fs)
    return sum(s for s in sizes if s < 100000)


def part_two(data):
    fs = reduce(lambda acc, c: interpret_cmd(acc, c), data, get_initial())
    sizes = get_dir_sizes(fs)
    difftofree = 30000000 - (70000000 - calc_size(fs, Path("/"), 0))
    return min(s for s in sizes if s > difftofree)
