from functools import partial, wraps
from pathlib import Path
from toolz import unique  # type: ignore


def move(coords, direction):
    if direction == "^":
        return [coords[0] + 1, coords[1]]
    if direction == "v":
        return [coords[0] - 1, coords[1]]
    if direction == ">":
        return [coords[0], coords[1] + 1]
    if direction == "<":
        return [coords[0], coords[1] - 1]


def visit(coords, directions):
    visited = [coords]
    for char in directions:
        coords = move(coords, char)
        visited.append(coords)
    return list(unique(map(str, visited)))


if __name__ == "__main__":

    raw = Path("input-03.txt").read_text()
    coords = [0, 0]
    # visited = [[0, 0]]
    """
    for char in raw:
        coords = move(coords, char)
        visited.append(coords)
    print(len(visited))
    assert len(visited) == len(raw) + 1
    print(len(list(unique([str(_) for _ in visited]))))
    """
    assert len(visit([9, 0], ">")) == 2
    assert len(visit([9, 0], "^>v<")) == 4
    assert len(visit([9, 0], "^v^v^v^v^v")) == 2
    print(len(visit([0, 0], raw.strip())))
    santa = raw[::2]
    robosanta = raw[1::2]

    def sp(txt):
        return txt[::2], txt[1::2]

    pt2 = partial(
        lambda s, r: len(list(unique(visit([0, 0], s) + visit([0, 0], r))))
    )
    assert pt2(*sp("^v")) == 3
    assert pt2(*sp("^>v<")) == 3
    assert pt2(*sp("^v^v^v^v^v")) == 11
    print(pt2(*sp(raw.strip())))

    # print(len(list(unique(visit([0, 0], santa) + visit([0, 0], robosanta)))))
"""
--- Day 3: Perfectly Spherical Houses in a Vacuum ---

Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and
then an elf at the North Pole calls him via radio and tells him where to move
next. Moves are always exactly one house to the north (^), south (v), east (>),
or west (<). After each move, he delivers another present to the house at his
new location.

However, the elf back at the north pole has had a little too much eggnog, and
so his directions are a little off, and Santa ends up visiting some houses more
than once. How many houses receive at least one present?

For example:

    > delivers presents to 2 houses: one at the starting location, and one to
    the east.
    ^>v< delivers presents to 4 houses in a square, including twice to the
    house at his starting/ending location.
    ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only
    2 houses.

Your puzzle answer was 2565.
--- Part Two ---

The next year, to speed up the process, Santa creates a robot version of
himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the
same starting house), then take turns moving based on instructions from the
elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

    ^v delivers presents to 3 houses, because Santa goes north, and then
    Robo-Santa goes south.
    ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up
    back where they started.
    ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one
    direction and Robo-Santa going the other.

Your puzzle answer was 2639.
"""
