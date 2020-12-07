import pdb
from functools import partial
from pathlib import Path
from string import digits as ascii_digits
import networkx  # type: ignore
from toolz import complement, compose_left, itemmap  # type: ignore

lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lcompact = partial(lfilter, None)


def parse(rule):
    color, contents = rule.split(" bags contain ")
    return color, contents


def parse_edges(rule, colormap, mygraph):
    color, contents = rule.split(" bags contain ")
    contents = contents.removesuffix(".")
    if "no other bags" in contents:
        return mygraph
    for edge in contents.split(","):
        mygraph = add_edge(mygraph, edge, color, colormap)
    return mygraph


def add_nodes(mygraph, mynodes):
    for key, value in mynodes.items():
        if key and value:
            mygraph.add_nodes_from([(key, {"color": value})])
    return mygraph


def add_edge(mygraph, edge, origincolor, colormap):
    edge = edge.removesuffix("bags").removesuffix("bag").strip()
    origincolornum = colormap.get(origincolor)
    num, tcolor = edge.split(" ", 1)
    for _ in range(int(num)):
        mygraph.add_edge(origincolornum, colormap.get(tcolor))
    return mygraph


def search(mygraph, mynode, prepreds):
    preds = list(mygraph.predecessors(mynode))
    if not preds:
        return prepreds
    for pred in preds:
        prepreds = prepreds + [pred] if pred not in prepreds else prepreds
    for sub in preds:
        prepreds = search(mygraph, sub, prepreds)
    return prepreds


def ssearch(mygraph, mynode, total):
    total = total + 1
    succs = list(mygraph.successors(mynode))
    for node in succs:
        paths = mygraph.number_of_edges(mynode, node)
        for _ in range(paths):
            total = total + ssearch(mygraph, node, 0)
    return total


def process(text):
    lines = lcompact(text.splitlines())
    nodes = lcompact([parse(rule)[0] for rule in lines])
    nodemap = dict(enumerate(nodes))
    color_to_node = itemmap(reversed, nodemap)
    graph = networkx.MultiDiGraph()
    populated = add_nodes(graph, nodemap)
    for rule in lines:
        populated = parse_edges(rule, color_to_node, populated)
    totals = search(populated, color_to_node.get("shiny gold"), [])
    assert len(totals) == 101
    print("Answer to part one: ", len(totals))
    totals2 = ssearch(populated, color_to_node.get("shiny gold"), 0)
    assert totals2 - 1 == 108636
    print("Answer to part two: ", totals2 - 1)


test_input = "\n".join(
    [
        "light red bags contain 1 bright white bag, 2 muted yellow bags.",
        "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
        "bright white bags contain 1 shiny gold bag.",
        "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
        "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
        "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
        "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
        "faded blue bags contain no other bags.",
        "dotted black bags contain no other bags.",
    ]
)

test_input2 = "\n".join(
    [
        "shiny gold bags contain 2 dark red bags.",
        "dark red bags contain 2 dark orange bags.",
        "dark orange bags contain 2 dark yellow bags.",
        "dark yellow bags contain 2 dark green bags.",
        "dark green bags contain 2 dark blue bags.",
        "dark blue bags contain 2 dark violet bags.",
        "dark violet bags contain no other bags.",
    ]
)


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer

    raw = Path("input-07.txt").read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    # test_result = process(test_input)
    # test_result2 = process(test_input2)
    process(raw)

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
