from toolz import pipe

from tadhg_utils import (
    p_lmap as cmap,  # Partial/curryable version of map that returns a list.
    splitstriplines,
)

two_test = [
    "",
    "██··██··██··██··██··██··██··██··██··██··",
    "███···███···███···███···███···███···███·",
    "████····████····████····████····████····",
    "█████·····█████·····█████·····█████·····",
    "██████······██████······██████······████",
    "███████·······███████·······███████·····",
]
two_answer = [
    "",
    "████··██··███···██····██·████···██·████·",
    "···█·█··█·█··█·█··█····█·█·······█····█·",
    "··█··█····███··█··█····█·███·····█···█··",
    "·█···█····█··█·████····█·█·······█··█···",
    "█····█··█·█··█·█··█·█··█·█····█··█·█····",
    "████··██··███··█··█··██··█·····██··████·",
]

TEST_ANSWERS = (13140, "\n".join(two_test))
PUZZLE_ANSWERS = (17940, "\n".join(two_answer))


def parse_line(line):
    if line.strip() == "noop":
        return [0]
    return [0, int(line.split(" ")[1].strip())]


def preprocess(data):
    procs = (splitstriplines, cmap(parse_line))
    return pipe(data, *procs)


def part_one(lines):
    data = lines[:]
    cycle, x = 0, 1
    values, stack = [], []

    while data or stack:
        cycle = cycle + 1

        exc = stack.pop(0) if stack else 0
        cmd = data.pop(0) if data else []

        stack = stack + cmd
        x = x + exc

        if (cycle - 20) % 40 == 0:
            values = values + [cycle * x]

    return sum(values)


def part_two(lines):
    data = lines[:]
    cycle = 0
    sprite = [0, 1, 2]
    lines, stack = [[]], []

    while data or stack:

        char = "█" if ((cycle) % 40) in sprite else "·"
        lines[-1].append(char)

        if len(lines[-1]) == 40:
            lines.append([])

        stack = stack + (data.pop(0) if data else [])

        exc = stack.pop(0) if stack else 0
        sprite = [pos + exc for pos in sprite]

        cycle = cycle + 1

    # Extra opening "\n" to make the runner harness print it nicely:
    return "\n" + "\n".join("".join(line) for line in lines).strip()
