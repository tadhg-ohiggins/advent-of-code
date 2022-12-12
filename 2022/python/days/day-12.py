from dataclasses import dataclass
from string import ascii_lowercase
import networkx as nx

from toolz import pipe

from tutils import trace, splitblocks, Point
from tadhg_utils import splitstriplines


@dataclass(frozen=True)
class HPoint(Point):
    height: int
    special: str

    def to_point(self):
        return Point(self.x, self.y)


TEST_ANSWERS = (31, 29)
PUZZLE_ANSWERS = (497, 492)


def make_points(lines):
    points = {}

    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            point = {"x": x, "y": y}
            if val == "S":
                point["height"] = 0
                point["special"] = "start"
            elif val == "E":
                point["height"] = 25
                point["special"] = "end"
            else:
                point["height"] = ascii_lowercase.index(val)
                point["special"] = ""
            points[(x, y)] = HPoint(**point)

    return points


def get_neighbors(pt):
    return (
        pt + Point(1, 0),
        pt + Point(-1, 0),
        pt + Point(0, 1),
        pt + Point(0, -1),
    )


def make_graph(points):
    G = nx.DiGraph()
    start, end = None, None
    for k, v in points.items():
        neighbors = []
        candidates = get_neighbors(v.to_point())
        for candidate in candidates:
            if tuple(candidate) in points:
                if v.height - points[tuple(candidate)].height >= -1:
                    neighbors.append(candidate)

        for n in neighbors:
            G.add_edge(tuple(v.to_point()), tuple(n))
        if v.special == "start":
            start = v.to_point()
        elif v.special == "end":
            end = v.to_point()

    return points, G, start, end


def preprocess(data):
    procs = [
        splitstriplines,
        make_points,
        make_graph,
    ]
    result = pipe(data, *procs)
    return result


def part_one(data):
    _, graph, start, end = data
    path = nx.shortest_path(graph, tuple(start), tuple(end))
    return len(path) - 1


def part_two(data):
    points, graph, _, end = data
    starts = {v.to_point() for v in points.values() if v.height == 0}
    steps = 10000
    for start in starts:
        try:
            path = nx.shortest_path(graph, tuple(start), tuple(end))
            if len(path) < steps:
                steps = len(path)
        except nx.exception.NetworkXNoPath:
            pass

    return steps - 1
