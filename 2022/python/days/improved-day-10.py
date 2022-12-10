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
    return [0] if line == "noop" else [0, int(line.split(" ")[1])]


def preprocess(data):
    procs = (splitstriplines, cmap(parse_line))
    return pipe(data, *procs)


def part_one(lines):
    data = lines[:]
    cycle, x = 0, 1
    values, stack = [], []

    # Unhappy that I couldn’t do ``while data or stack:`` here instead, but
    # even though that works—because it doesn’t alter what goes into `values`—I
    # still don’t like the fact that it runs unnecessary iterations.
    while cycle < 240:

        cycle = cycle + 1
        x = x + (stack.pop(0) if stack else 0)
        stack = stack + (data.pop(0) if data else [])

        if (cycle - 20) % 40 == 0:
            values = values + [cycle * x]
        if cycle >= 240:
            print(cycle)

    return sum(values)


def part_two(commands):
    data = commands[:]
    cycle, x = 0, 1
    lines, stack = [[]], []

    # Unhappy that I couldn’t do ``while data or stack:`` here instead,  but
    # there’s an off-by-one error in here that writes a trailing dot if I don’t
    # stop it at cycle == 239.
    while cycle < 240:

        cycle = cycle + 1
        x = x + (stack.pop(0) if stack else 0)
        stack = stack + (data.pop(0) if data else [])

        char = "█" if (cycle - 1) % 40 in (x - 1, x, x + 1) else "·"
        lines[-1].append(char)

        if len(lines[-1]) == 40:
            lines.append([])

    # Extra opening "\n" to make the runner harness print it nicely:
    return "\n" + "\n".join("".join(line) for line in lines).strip()
