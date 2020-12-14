from collections import Counter, defaultdict
from functools import partial, reduce
from itertools import product
from pathlib import Path
from toolz import (  # type: ignore
    compose_left,
    iterate,
)


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lcompact = partial(lfilter, None)
splitstrip = compose_left(str.split, partial(lmap, str.strip), lcompact)
make_incr = lambda: partial(next, iterate(lambda x: x + 1, 0))


def parsecommand(line):
    regstr, value = splitstrip(line, " = ")
    register = regstr.removeprefix("mem[").removesuffix("]")
    return {"r": int(register), "v": int(value)}


def int_to_36bit(i):
    return bin(i).removeprefix("0b").zfill(36)


def get_mask(maskstr):
    vals = {}
    for i, bit in enumerate(maskstr.removeprefix("0b")):
        if bit in ("0", "1"):
            vals[i] = bit
    return vals


def apply_mask(mask, binstr):
    arr = list(binstr)
    for key in mask:
        arr[key] = mask[key]
    return "".join(arr)


def apply_mask2(registers, mask, reg, val):
    arr = list(mask)
    newarr = list(reg)
    for i, bit in enumerate(arr):
        if bit in ("1", "X"):
            newarr[i] = bit
    addrs = []
    combos = newarr.count("X")
    if not combos:
        addrs = ["".join(newarr)]
    else:
        pairs = [[0, 1]] * combos
        prods = [*product(*pairs)]

        for prd in prods:
            newnewarr = []
            count = 0
            for i, c in enumerate(newarr):
                if c == "X":
                    newnewarr.append(str(prd[count]))
                    count = count + 1
                else:
                    newnewarr.append(newarr[i])
            addrs.append("".join(newnewarr))
    for addr in addrs:
        registers[int(addr, 2)] = val
    return registers


def parse_lines(lines):
    mask = splitstrip(lines[0], " = ")[1].removeprefix("0b")
    commands = lmap(parsecommand, lines[1:])
    return mask, commands


def get_programs(lines):
    arrays = defaultdict(list)
    ctr = make_incr()
    i = None
    for line in lines:
        if line.startswith("mask"):
            i = ctr()
        arrays[i].append(line)
    return arrays


def process_program(registers, lines):
    maskstr, commands = parse_lines(lines)
    mask = get_mask(maskstr)
    for cmd in commands:
        registers[cmd["r"]] = int(apply_mask(mask, int_to_36bit(cmd["v"])), 2)

    return registers


def memwrite(mask, registers, command):
    reg, val = command["r"], command["v"]
    return apply_mask2(registers, mask, int_to_36bit(reg), val)


def process_program2(registers, lines):
    mask, commands = parse_lines(lines)
    mwrite = partial(memwrite, mask)
    return reduce(mwrite, commands, registers)


def sumreg(registers):
    return sum([v for v in registers.values() if v])


def process(text):
    lines = lcompact(text.splitlines())
    programs = get_programs(lines)
    answer = sumreg(reduce(process_program, [*programs.values()], {}))
    assert answer == 12408060320841

    answer_two = sumreg(reduce(process_program2, [*programs.values()], {}))
    assert answer_two == 4466434626828
    print("Answer one:", answer)
    print("Answer two:", answer_two)


if __name__ == "__main__":
    process(Path("input-14.txt").read_text().strip())
