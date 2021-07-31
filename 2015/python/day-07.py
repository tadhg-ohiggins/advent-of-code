from tutils import pdb
from tutils import subprocess
from tutils import Counter
from tutils import partial
from tutils import reduce
from tutils import wraps
from tutils import count
from tutils import groupby
from tutils import product
from tutils import prod
from tutils import itemgetter
from tutils import Path
from tutils import ascii_lowercase
from tutils import ascii_digits
from tutils import Any
from tutils import Callable
from tutils import Dict
from tutils import List
from tutils import Iterable
from tutils import IterableS
from tutils import Optional
from tutils import Sequence
from tutils import OInt
from tutils import ODict
from tutils import UListStr
from tutils import Tuple
from tutils import Union
from tutils import hexc
from tutils import compose_left
from tutils import concat
from tutils import curry
from tutils import do
from tutils import excepts
from tutils import iterate
from tutils import keyfilter
from tutils import pluck
from tutils import pipe
from tutils import sliding_window
from tutils import toolz_pick
from tutils import toolz_omit
from tutils import omit
from tutils import pick
from tutils import valmap
from tutils import valfilter
from tutils import add_debug
from tutils import add_debug_list
from tutils import run_process
from tutils import until_stable
from tutils import oxford
from tutils import excepts_wrap
from tutils import nextwhere
from tutils import noncontinuous
from tutils import lnoncontinuous
from tutils import lfilter
from tutils import lconcat
from tutils import lcompact
from tutils import lmap
from tutils import lpluck
from tutils import lstrip
from tutils import splitstrip
from tutils import splitstriplines
from tutils import seq_to_dict
from tutils import split_to_dict
from tutils import c_map
from tutils import c_lmap
from tutils import is_char_az
from tutils import is_char_hex
from tutils import is_char_az09
from tutils import filter_str
from tutils import filter_az
from tutils import filter_az09
from tutils import filter_hex
from tutils import add_pprint
from tutils import add_pprinting
from tutils import make_incrementer
from tutils import adjacent_transforms
from tutils import load_input
from tutils import process_input
from tutils import tests

from tutils import load_and_process_input
from tutils import run_tests


""" END HELPER FUNCTIONS """


DAY = "07"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 123
TA2 = None
ANSWER1 = 16076
ANSWER2 = 2797


def bw_and(a: int, b: int) -> int:
    return a & b


def bw_lshift(a: int, b: int) -> int:
    return a << b


def bw_rshift(a: int, b: int) -> int:
    return a >> b


def bw_or(a: int, b: int) -> int:
    return a | b


def bw_not(a: int) -> int:
    regsize = 0b1111111111111111
    assert regsize == 65535
    return regsize - a


commands: Dict[str, Callable] = {
    "AND": bw_and,
    "LSHIFT": bw_lshift,
    "NOT": bw_not,
    "RSHIFT": bw_rshift,
    "OR": bw_or,
    # "PASSTHRU",
}


countx = 0


def process_one(lines: List[str]) -> int:
    return solver({}, lines)["a"]


def first_pass(lines: List[str]) -> dict:
    reducer = lambda a, b: a | parse_line(b)
    return reduce(reducer, lines, {})


def format_cmd(elements: List[str]) -> List[Union[int, str]]:
    if len(elements) == 1:
        return {"values": [int_or_command(elements[0])], "command": None}

    if len(elements) == 2:
        assert elements[0] == "NOT"
        return {
            "values": [int_or_command(elements[1])],
            "command": "NOT",
        }

    if len(elements) == 3:
        assert elements[1] in commands
        return {
            "values": [
                int_or_command(elements[0]),
                int_or_command(elements[2]),
            ],
            "command": elements[1],
        }


def parse_line(line: str) -> dict:
    src, target = splitstrip(line, "->")
    elements = splitstrip(src, " ")
    return {target: format_cmd(elements)}


def int_or_command(instr: str) -> Union[int, str]:
    return int(instr) if instr.isdigit() else instr


def reducer(mapping: dict, line: str) -> dict:
    # Do one line at a time, then repeat.
    target, value = get_target_and_value(mapping, line)
    if target is not False and value is not False:
        mapping = mapping | {target: value}
    return mapping


def solver(gates: dict, lines: List[str]) -> dict:
    candidate = reduce(reducer, lines, gates)

    if len(candidate) == len(lines):
        return candidate

    return solver(candidate, lines)


def get_target_and_value(
    gates: dict, value: str
) -> Union[Tuple[str, int], Tuple[bool, bool]]:
    src, target = splitstrip(value, "->")
    elements = splitstrip(src, " ")

    if len(elements) == 1:
        source = resolve_value(gates, elements[0])
        if source is not False:
            return target, source

    if len(elements) == 2:
        assert elements[0] == "NOT"
        if elements[1] in gates:
            return target, bw_not(gates[elements[1]])

    if len(elements) == 3:
        assert elements[1] in commands
        source1 = resolve_value(gates, elements[0])
        source2 = resolve_value(gates, elements[2])
        if source1 is not False and source2 is not False:
            return target, commands[elements[1]](source1, source2)

    return False, False


def resolve_value(gates: dict, initial: Any) -> Union[int, bool]:
    return int(initial) if initial.isdigit() else gates.get(initial, False)


def process_two(lines: List[str], answer_one) -> int:
    new_b = f"{answer_one} -> b"
    wires = lmap(lambda x: new_b if x == "19138 -> b" else x, lines)
    return solver({}, wires)["a"]


def cli_main() -> None:
    input_funcs = [splitstriplines]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_one = process_one(data)
    if ANSWER1 is not None:
        if answer_one != ANSWER1:
            pdb.set_trace()

        assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    if ANSWER1 is not None:
        answer_two = process_two(data, answer_one)
        if ANSWER2 is not None:
            if answer_two != ANSWER2:
                pdb.set_trace()
            assert answer_two == ANSWER2
        print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()


"""
--- Day 7: Some Assembly Required ---

This year, Santa brought little Bobby Tables a set of wires and bitwise logic
gates! Unfortunately, little Bobby is a little under the recommended age range,
and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit
signal (a number from 0 to 65535). A signal is provided to each wire by a gate,
another wire, or some specific value. Each wire can only get a signal from one
source, but can provide its signal to multiple destinations. A gate provides no
signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts together:
    x AND y -> z means to connect wires x and y to an AND gate, and then
    connect its output to wire z.

For example:

    123 -> x means that the signal 123 is provided to wire x.
    x AND y -> z means that the bitwise AND of wire x and wire y is provided to
        wire z.
    p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and
        then provided to wire q.
    NOT e -> f means that the bitwise complement of the value from wire e is
        provided to wire f.

Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If, for
some reason, you'd like to emulate the circuit instead, almost all programming
languages (for example, C, JavaScript, or Python) provide operators for these
gates.

For example, here is a simple circuit:

123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i

After it is run, these are the signals on the wires:

d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456

In little Bobby's kit's instructions booklet (provided as your puzzle input),
what signal is ultimately provided to wire a?

Your puzzle answer was 16076.

--- Part Two ---

Now, take the signal you got on wire a, override wire b to that signal, and
reset the other wires (including wire a). What new signal is ultimately
provided to wire a?

Your puzzle answer was 2797.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your Advent calendar and try another
puzzle.

If you still want to see it, you can get your puzzle input.

You can also [Shareon Twitter Mastodon] this puzzle.
"""
