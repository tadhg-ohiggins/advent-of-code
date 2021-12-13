from functools import cache, partial, reduce
from math import prod
import pdb
import aoc
import networkx as nx
from toolz import keyfilter

from aoc import Point, adjacent_transforms, generate_bounded_coords
from tadhg_utils import (
    lcompact,
    lconcat,
    lfilter,
    lmap,
    splitstrip,
    splitstriplines,
)


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 17
TA2 = None
A1 = 631
A2 = [
    "####.####.#....####...##..##..###..####",
    "#....#....#....#.......#.#..#.#..#.#...",
    "###..###..#....###.....#.#....#..#.###.",
    "#....#....#....#.......#.#.##.###..#...",
    "#....#....#....#....#..#.#..#.#.#..#...",
    "####.#....####.#.....##...###.#..#.#...",
]


def parse_instruction(instruction):
    axis, value = instruction.replace("fold along ", "").split("=")
    return {"axis": axis, "value": int(value)}


def parse_data(data):
    raw_coords, raw_instructions = data.split("\n\n")
    coords = lmap(Point.from_string, splitstriplines(raw_coords))
    instructions = lmap(parse_instruction, splitstriplines(raw_instructions))

    return (coords, instructions)


def splity(coords, instruction, lims):
    _, ymax = lims
    splitline = instruction["value"]
    top_half = lfilter(lambda pt: pt.y < splitline, coords)
    bottom_half = lfilter(lambda pt: pt.y > splitline, coords)
    for point in bottom_half:
        new_point = Point(x=point.x, y=ymax - point.y)
        if new_point not in top_half:
            top_half.append(new_point)
    return top_half


def splitx(coords, instruction, lims):
    xmax, _ = lims
    splitline = instruction["value"]
    left_half = lfilter(lambda pt: pt.x < splitline, coords)
    right_half = lfilter(lambda pt: pt.x > splitline, coords)
    for point in right_half:
        new_point = Point(x=xmax - point.x, y=point.y)
        if new_point not in left_half:
            left_half.append(new_point)
    return left_half


def follow_instructions(coords, instruction, lims):
    if instruction["axis"] == "y":
        return splity(coords, instruction, lims)
    if instruction["axis"] == "x":
        return splitx(coords, instruction, lims)
    raise UserWarning("Unknown axis")


def process_one(data):
    coords, instructions = data
    xmax = sorted(coords, key=lambda p: p.x)[-1].x
    ymax = sorted(coords, key=lambda p: p.y)[-1].y
    count = 0
    for instruction in instructions:
        coords = follow_instructions(coords, instruction, (xmax, ymax))
        count = count + 1
        if count == 1:
            return len(coords)
        xmax = sorted(coords, key=lambda p: p.x)[-1].x
        ymax = sorted(coords, key=lambda p: p.y)[-1].y

    return data


def coords_to_lines(coords, lims):
    grid = [
        Point(*_) for _ in generate_bounded_coords([0, 0], [lims[0], lims[1]])
    ]
    lines = []
    for i in range(lims[1] + 1):
        line = ""
        for pt in filter(lambda p: p.y == i, grid):
            m = "#" if pt in coords else "."
            line = line + m
        lines.append(line)
        print(line)

    return lines


def process_two(data):
    coords, instructions = data
    xmax = sorted(coords, key=lambda p: p.x)[-1].x
    ymax = sorted(coords, key=lambda p: p.y)[-1].y
    for instruction in instructions:
        coords = follow_instructions(coords, instruction, (xmax, ymax))
        xmax = sorted(coords, key=lambda p: p.x)[-1].x
        ymax = sorted(coords, key=lambda p: p.y)[-1].y

    return coords_to_lines(coords, (xmax, ymax))


def cli_main() -> None:
    input_funcs = [parse_data]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    print(result_one)
    result_two = process_two(data)
    aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
"""
"""
