from math import inf
from string import ascii_lowercase
import networkx as nx

from tadhg_utils import splitstriplines


TEST_ANSWERS = (31, 29)
PUZZLE_ANSWERS = (497, 492)


def get_height(val):
    if val == "S":
        return 0
    if val == "E":
        return 25
    return ascii_lowercase.index(val)


def make_graph(lines, start_qualifiers):
    graph = nx.DiGraph()
    xlim, ylim = len(lines[0]), len(lines)
    starts = []

    def add_if_step(origin, origin_val, candidate):
        nval = lines[candidate[1]][candidate[0]]
        if get_height(origin_val) - get_height(nval) >= -1:
            graph.add_edge(origin, candidate)

    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            if x > 0:
                add_if_step((x, y), val, (x - 1, y))
            if y > 0:
                add_if_step((x, y), val, (x, y - 1))
            if (x + 1) < xlim:
                add_if_step((x, y), val, (x + 1, y))
            if (y + 1) < ylim:
                add_if_step((x, y), val, (x, y + 1))

            if val in start_qualifiers:
                starts.append((x, y))
            elif val == "E":
                end = (x, y)

    return graph, starts, end


preprocess = splitstriplines


def part_one(data):
    graph, starts, end = make_graph(data, ("S",))
    return len(nx.shortest_path(graph, starts[0], end)) - 1


def part_two(data):
    graph, starts, end = make_graph(data, ("S", "a"))
    steps = inf
    for start in starts:
        try:
            path = nx.shortest_path(graph, start, end)
        except nx.exception.NetworkXNoPath:
            continue
        steps = min(steps, len(path))

    return steps - 1
