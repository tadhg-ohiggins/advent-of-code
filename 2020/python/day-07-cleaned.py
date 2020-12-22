from functools import partial, reduce
from typing import List, Tuple
from networkx import MultiDiGraph  # type: ignore
from toolz import itemmap  # type: ignore
from tutils import (
    load_and_process_input,
    run_tests,
    splitstrip,
    splitstriplines,
)

DAY = "07"
INPUT = f"input-{DAY}.txt"
TEST = f"test-input-{DAY}.txt"
TA1 = 4
TA2 = None
ANSWER1 = 101
ANSWER2 = 108636


def parse(rule: str) -> Tuple[str, str]:
    color, contents = splitstrip(rule, "bags contain")
    return color, contents


def add_nodes(mygraph: MultiDiGraph, mynodes: dict) -> MultiDiGraph:
    for key, value in mynodes.items():
        if key and value:
            mygraph.add_nodes_from([(key, {"color": value})])
    return mygraph


def add_edge(
    mygraph: MultiDiGraph, edge: str, origincolor: str, colormap: dict
) -> MultiDiGraph:
    edge = reduce(str.removesuffix, [" bags", " bag"], edge)
    origincolornum = colormap.get(origincolor)
    num, tcolor = edge.split(" ", 1)
    for _ in range(int(num)):
        mygraph.add_edge(origincolornum, colormap.get(tcolor))
    return mygraph


def parse_edges(
    colormap: dict, mygraph: MultiDiGraph, rule: str
) -> MultiDiGraph:
    color, contents = parse(rule)
    contents = contents.removesuffix(".")
    if "no other bags" in contents:
        return mygraph
    for edge in splitstrip(contents, ","):
        mygraph = add_edge(mygraph, edge, color, colormap)
    return mygraph


def build_graph(rules: List[str]) -> Tuple[MultiDiGraph, dict]:
    """
    Rather than building the graph so that every individual bag is represented
    by a node, and colored, and doing the calculations based on colors in the
    graph, I did it so that every type of bag was one node, and the connections
    between the types of bag were represented by multiple edges. This is
    probably not the best way to do it, but it does work for these use cases.
    """
    nodes = [parse(rule)[0] for rule in rules]
    nodemap = dict(enumerate(nodes))
    color_to_node = itemmap(reversed, nodemap)
    noded = add_nodes(MultiDiGraph(), nodemap)
    edged = reduce(partial(parse_edges, color_to_node), rules, noded)
    return (edged, color_to_node)


def predecessor_search(mygraph: MultiDiGraph, mynode: str, preds: set) -> set:
    for node in mygraph.predecessors(mynode):
        preds = preds | {node}
        preds = predecessor_search(mygraph, node, preds)
    return preds


def successor_search(mygraph: MultiDiGraph, mynode: str, total: int) -> int:
    total = total + 1
    for node in mygraph.successors(mynode):
        paths = mygraph.number_of_edges(mynode, node)
        num_descendants = successor_search(mygraph, node, 0)
        total = total + (num_descendants * paths)
    return total


def process_one(graph_and_key: Tuple[MultiDiGraph, dict]) -> int:
    graph, target = graph_and_key[0], graph_and_key[1].get("shiny gold", "")
    return len(predecessor_search(graph, target, set()))


def process_two(graph_and_key: Tuple[MultiDiGraph, dict]) -> int:
    graph, target = graph_and_key[0], graph_and_key[1].get("shiny gold", "")
    return successor_search(graph, target, -1)


def cli_main() -> None:
    input_funcs = [splitstriplines, build_graph]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process_two(data)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
"""
--- Day 7: Handy Haversacks ---

You land at the regional airport in time for your next flight. In fact, it
looks like you'll even have time to grab some food: all flights are currently
delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being
enforced about bags and their contents; bags must be color-coded and must
contain specific quantities of other color-coded bags. Apparently, nobody
responsible for these regulations considered how long they would take to
enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.

These rules specify the required contents for 9 bag types. In this example,
every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded
blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag,
how many different bag colors would be valid for the outermost bag? (In other
words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

    A bright white bag, which can hold your shiny gold bag directly.
    A muted yellow bag, which can hold your shiny gold bag directly, plus some
    other bags.
    A dark orange bag, which can hold bright white and muted yellow bags,
    either of which could then hold your shiny gold bag.
    A light red bag, which can hold bright white and muted yellow bags, either
    of which could then hold your shiny gold bag.

So, in this example, the number of bag colors that can eventually contain at
least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The
list of rules is quite long; make sure you get all of it.)

Your puzzle answer was 101.
--- Part Two ---

It's getting pretty expensive to fly these days - not because of ticket prices,
but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

    faded blue bags contain 0 other bags.
    dotted black bags contain 0 other bags.
    vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted
    black bags.
    dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black
    bags.

So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags
within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 +
1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper
than this example; be sure to count all of the bags, even if the nesting
becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.

In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?

Your puzzle answer was 108636.
"""
