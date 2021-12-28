from functools import cache, partial, reduce
from math import prod
import pdb
import aoc
import networkx as nx
from toolz import keyfilter

from aoc import Point, adjacent_transforms
from tadhg_utils import (
    lcompact,
    lconcat,
    lfilter,
    lmap,
    splitstrip,
    splitstriplines,
)


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 226
TA2 = 3509
A1 = 5333
A2 = None


testdata1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

testdata = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""


def process_one(data):
    # About 40m to complete the first one.
    # data = splitstriplines(testdata)
    connections = [_.split("-") for _ in data]
    nodes = set(lconcat(connections))
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    for edge in connections:
        graph.add_edge(*edge)

    paths = find_all_paths(graph, "start", "end")
    return len(paths)


def find_all_paths(graph, start, end):
    path = []
    paths = []
    queue = [(start, end, path)]
    while queue:
        start, end, path = queue.pop()
        path = path + [start]
        if start == end:
            paths.append(path)
        for node in set(graph[start]):
            if node.islower() and node not in path:
                queue.append((node, end, path))
            elif node.isupper():
                queue.append((node, end, path))
    return paths


def find_all_paths2(graph, start, end):
    path = []
    paths = []
    queue = [(start, end, path)]
    while queue:
        start, end, path = queue.pop()
        path = path + [start]
        if start == end:
            paths.append(path)
        for node in set(graph[start]):
            if node in ("start", "end"):
                if node not in path:
                    queue.append((node, end, path))
            elif node.islower():
                lcnodes = lfilter(
                    lambda x: x not in ("start", "end") and x.islower(), path
                )
                if len(lcnodes) == len(set(lcnodes)) and path.count(node) <= 1:
                    queue.append((node, end, path))
                elif (
                    len(lcnodes) - 1 == len(set(lcnodes))
                    and path.count(node) < 1
                ):
                    queue.append((node, end, path))

            elif node.isupper():
                queue.append((node, end, path))
    return paths


def process_two(data):
    # About 50m to complete both.
    # data = splitstriplines(testdata1)
    connections = [_.split("-") for _ in data]
    nodes = set(lconcat(connections))
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    for edge in connections:
        graph.add_edge(*edge)

    paths = find_all_paths2(graph, "start", "end")
    return len(paths)


def cli_main() -> None:
    input_funcs = [splitstriplines]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    print(result_one)
    result_two = process_two(data)
    aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
"""
"""
