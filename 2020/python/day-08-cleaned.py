from typing import Callable, List, Tuple
from tutils import (
    UBoolInt,
    load_and_process_input,
    make_incrementer,
    run_tests,
    splitstrip,
    splitstriplines,
)

DAY = "08"
INPUT = f"input-{DAY}.txt"
TEST = f"test-input-{DAY}.txt"
TA1 = None
TA2 = None
ANSWER1 = 1675
ANSWER2 = 1532


LStr = List[str]
LInt = List[int]


def parse_line(line: str, current: int, total: int) -> Tuple[int, int]:
    command, amount = splitstrip(line, " ")
    if command in ("nop", "acc"):
        nextindex = current + 1
    if command == "jmp":
        nextindex = current + int(amount)
    if command == "acc":
        total = total + int(amount)
    return nextindex, total


def process_lines(
    lines: LStr, current: int, total: int, seen: LInt, return_on_fail: bool
) -> UBoolInt:
    if current >= len(lines):
        return total
    seen = seen + [current]
    nextindex, total = parse_line(lines[current], current, total)
    if nextindex in seen:
        return total if return_on_fail else False
    return process_lines(lines, nextindex, total, seen, return_on_fail)


def command_swap(text: str, command_one: str, command_two: str) -> str:
    if command_one in text:
        return text.replace(command_one, command_two)
    return text.replace(command_two, command_one)


def change_lines(lines: List[str], origlines: List[str], ctr: Callable) -> int:
    """
    The completely naive approach: just go through the list of lines, changing
    one at a time, until you find the change that makes the whole thing go
    through without a loop.

    The very first obvious optimization would be skip lines that don't contain
    one of the two commands that can be swapped--right now, it runs the entire
    set again even if the most recent run of command_swap did nothing.
    """
    total = process_lines(lines, 0, 0, [], False)
    if total:
        return total
    newlines = origlines[:]
    i = ctr()
    newlines[i] = command_swap(newlines[i], "jmp", "nop")
    return change_lines(newlines, origlines, ctr)


def process_one(lines: List[str]) -> UBoolInt:
    return process_lines(lines[:], 0, 0, [], True)


def process_two(lines: List[str]) -> int:
    ctr = make_incrementer()
    return change_lines(lines[:], lines[:], ctr)


def cli_main() -> None:
    input_funcs = [splitstriplines]
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
--- Day 8: Handheld Halting ---

Your flight to the major airline hub reaches cruising altitude without
incident. While you consider checking the in-flight menu for one of those
drinks that come with a little umbrella, you are interrupted by the kid sitting
next to you.

Their handheld game console won't turn on! They ask if you can take a look.

You narrow the problem down to a strange infinite loop in the boot code (your
puzzle input) of the device. You should be able to fix it, but first you need
to be able to run the code in isolation.

The boot code is represented as a text file with one instruction per line of
text. Each instruction consists of an operation (acc, jmp, or nop) and an
argument (a signed number like +4 or -20).

    acc increases or decreases a single global value called the accumulator by
    the value given in the argument. For example, acc +7 would increase the
    accumulator by 7. The accumulator starts at 0. After an acc instruction,
    the instruction immediately below it is executed next.

    jmp jumps to a new instruction relative to itself. The next instruction to
    execute is found using the argument as an offset from the jmp instruction;
    for example, jmp +2 would skip the next instruction, jmp +1 would continue
    to the instruction immediately below it, and jmp -20 would cause the
    instruction 20 lines above to be executed next.

    nop stands for No OPeration - it does nothing. The instruction immediately
    below it is executed next.

For example, consider the following program:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6

These instructions are visited in this order:

nop +0  | 1
acc +1  | 2, 8(!)
jmp +4  | 3
acc +3  | 6
jmp -3  | 7
acc -99 |
acc +1  | 4
jmp -4  | 5
acc +6  |

First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1
(acc +1) and jmp +4 sets the next instruction to the other acc +1 near the
bottom. After it increases the accumulator from 1 to 2, jmp -4 executes,
setting the next instruction to the only acc +3. It sets the accumulator to 5,
and jmp -3 causes the program to continue back at the first acc +1.

This is an infinite loop: with this sequence of jumps, the program will run
forever. The moment the program tries to run any instruction a second time, you
know it will never terminate.

Immediately before the program would run an instruction a second time, the
value in the accumulator is 5.

Run your copy of the boot code. Immediately before any instruction is executed
a second time, what value is in the accumulator?

Your puzzle answer was 1675.

--- Part Two ---

After some careful analysis, you believe that exactly one instruction is
corrupted.

Somewhere in the program, either a jmp is supposed to be a nop, or a nop is
supposed to be a jmp. (No acc instructions were harmed in the corruption of
this boot code.)

The program is supposed to terminate by attempting to execute an instruction
immediately after the last instruction in the file. By changing exactly one jmp
or nop, you can repair the boot code and make it terminate correctly.

For example, consider the same program from above:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6

If you change the first instruction from nop +0 to jmp +0, it would create a
single-instruction infinite loop, never leaving that instruction. If you change
almost any of the jmp instructions, the program will still eventually find
another jmp instruction and loop forever.

However, if you change the second-to-last instruction (from jmp -4 to nop -4),
the program terminates! The instructions are visited in this order:

nop +0  | 1
acc +1  | 2
jmp +4  | 3
acc +3  |
jmp -3  |
acc -99 |
acc +1  | 4
nop -4  | 5
acc +6  | 6

After the last instruction (acc +6), the program terminates by attempting to
run the instruction below the last instruction in the file. With this change,
after the program terminates, the accumulator contains the value 8 (acc +1, acc
+1, acc +6).

Fix the program so that it terminates normally by changing exactly one jmp (to
nop) or nop (to jmp). What is the value of the accumulator after the program
terminates?

Your puzzle answer was 1532.
"""
