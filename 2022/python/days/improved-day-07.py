from functools import partial
from pathlib import Path

from toolz import pipe

from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that return a list.
    splitstriplines,
    splitstrip,
)


TEST_ANSWERS = (95437, 24933642)
PUZZLE_ANSWERS = (1915606, 5025657)


def get_path_info(cmds):
    path, paths = Path("/"), {}
    for cmd in cmds:
        if cmd[0].startswith("cd"):
            path = Path(path, cmd[0][3:].strip()).resolve()
        elif cmd[0].startswith("ls"):
            files = filter(lambda c: not c.startswith("dir"), cmd[1:])
            fsize = sum(int(fd.split(" ", 1)[0]) for fd in files)
            paths[path] = fsize
    return paths


def get_size(paths, path):
    return sum(paths[p] for p in paths if str(p).startswith(str(path)))


def preprocess(data):
    procs = (
        str.strip,
        partial(splitstrip, sep="$"),
        cmap(splitstriplines),
    )
    return pipe(data, *procs)


def part_one(data):
    paths = get_path_info(data)
    sizes = (get_size(paths, p) for p in paths)
    return sum(s for s in sizes if s < 100000)


def part_two(data):
    paths = get_path_info(data)
    sizes = [get_size(paths, p) for p in paths]
    difftofree = 30000000 - (70000000 - sizes[0])
    return min(s for s in sizes if s > difftofree)
