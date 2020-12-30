from functools import partial, reduce
from itertools import product
from typing import Callable, Iterable, List, Tuple
from more_itertools import split_before

from tutils import (
    lmap,
    splitstrip,
    splitstriplines,
    load_and_process_input,
    run_tests,
)

DAY = "14"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 165
TA2 = 208
ANSWER1 = 12408060320841
ANSWER2 = 4466434626828


def int_to_36bit(i: int) -> str:
    return bin(i).removeprefix("0b").zfill(36)


def parsecommand(line: str) -> dict:
    regstr, value = splitstrip(line, " = ")
    register = int(regstr.removeprefix("mem[").removesuffix("]"))
    return {"r": int(register), "v": int(value)}


def parse_group(group: List[str]) -> Tuple[str, List[dict]]:
    mask = splitstrip(group[0], " = ")[1]
    commands = lmap(parsecommand, group[1:])
    return mask, commands


def lines_to_programs(lines: List[str]) -> List[Tuple[str, List[dict]]]:
    """
    Programs will be represented as two-part tuples. The first part is the
    mask, a string. The second part is a list of registers and values,
    represented by a dict with the keys "r" and "v".
    """
    return lmap(parse_group, split_before(lines, lambda s: s[:4] == "mask"))


def apply_mask(maskstr: str, registers: dict, command: dict) -> dict:
    register, value = command["r"], int_to_36bit(command["v"])
    mask = {i: bit for i, bit in enumerate(maskstr) if bit in ("0", "1")}
    masked = [mask.get(i, x) for i, x in enumerate(value)]
    return {**registers, **{register: int("".join(masked), 2)}}


def process_program(func: Callable, registers: dict, program: Tuple) -> dict:
    mask, commands = program
    masker = partial(func, mask)
    return reduce(masker, commands, registers)


def generate_combination_addresses(base_address: List[str]) -> Iterable[str]:
    # For every X in the string, we need all combinations of 1 and 0, so
    # count(X) ** 2 of them.
    xcount = base_address.count("X")
    if not xcount:
        return ["".join(base_address)]
    combinations = product(*[[0, 1]] * xcount)
    # For each X, replace it with the correspondiing bit from the combo:
    replace_x = lambda x, y: x.replace("X", str(y), 1)
    replace_all_xs = lambda b: reduce(replace_x, b, "".join(base_address))
    return map(replace_all_xs, combinations)


def apply_mask2(mask: str, registers: dict, command: dict) -> dict:
    address, value = list(int_to_36bit(command["r"])), command["v"]
    masked = [b if b in ("1", "X") else address[i] for i, b in enumerate(mask)]

    # This iterative version is faster than a dict comprehension:
    for addr in generate_combination_addresses(masked):
        registers[int(addr, 2)] = value
    return registers


def process_one(programs: List[Tuple]) -> int:
    process_program1 = partial(process_program, apply_mask)
    return sum(reduce(process_program1, programs, {}).values())


def process_two(programs: List[Tuple]) -> int:
    process_program2 = partial(process_program, apply_mask2)
    return sum(reduce(process_program2, programs, {}).values())


def cli_main() -> None:
    input_funcs = [splitstriplines, lines_to_programs]
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
