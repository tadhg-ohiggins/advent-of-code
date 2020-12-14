from collections import Counter, defaultdict
from functools import partial, reduce
from itertools import product
from pathlib import Path
from more_itertools import split_before
from toolz import compose_left, iterate  # type: ignore


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lcompact = partial(lfilter, None)
splitstrip = compose_left(str.split, partial(lmap, str.strip), lcompact)
make_incr = lambda: partial(next, iterate(lambda x: x + 1, 0))
sum_values = lambda d: sum(d.values())
int_to_36bit = lambda i: bin(i).removeprefix("0b").zfill(36)


def parsecommand(line):
    regstr, value = splitstrip(line, " = ")
    register = int(regstr.removeprefix("mem[").removesuffix("]"))
    return {"r": int(register), "v": int(value)}


def parse_lines(lines):
    mask = splitstrip(lines[0], " = ")[1].removeprefix("0b")
    commands = lmap(parsecommand, lines[1:])
    return mask, commands


def apply_mask(mask, registers, command):
    register, value = command["r"], int_to_36bit(command["v"])
    masked = [mask.get(i, x) for i, x in enumerate(value)]
    return registers | {register: int("".join(masked), 2)}


def process_program(registers, lines):
    maskstr, commands = parse_lines(lines)
    mask = {i: bit for i, bit in enumerate(maskstr) if bit in ("0", "1")}
    masker = partial(apply_mask, mask)
    return reduce(masker, commands, registers)


def generate_combination_addresses(base_address):
    # For every X in the string, we need all combinations of 1 and 0, so
    # count(X) ** 2 of them.
    xcount = base_address.count("X")
    if not xcount:
        return [base_address]
    combinations = product(*[[0, 1]] * xcount)
    # For each X, replace it with the correspondiing bit from the combo:
    replace_x = lambda x, y: x.replace("X", str(y), 1)
    replace_all_xs = lambda b: reduce(replace_x, b, "".join(base_address))
    return map(replace_all_xs, combinations)


def apply_mask2(mask, registers, command):
    address, value = list(int_to_36bit(command["r"])), command["v"]
    masked = [b if b in ("1", "X") else address[i] for i, b in enumerate(mask)]

    for addr in generate_combination_addresses(masked):
        registers[int(addr, 2)] = value
    return registers


def process_program2(registers, lines):
    mask, commands = parse_lines(lines)
    masker = partial(apply_mask2, mask)
    return reduce(masker, commands, registers)


def process(text):
    lines = lcompact(text.splitlines())
    programs = list(split_before(lines, lambda s: s.startswith("mask")))
    answer = sum_values(reduce(process_program, programs, {}))
    assert answer == 12408060320841

    answer_two = sum_values(reduce(process_program2, programs, {}))
    assert answer_two == 4466434626828
    print("Answer one:", answer)
    print("Answer two:", answer_two)


if __name__ == "__main__":
    process(Path("input-14.txt").read_text().strip())
