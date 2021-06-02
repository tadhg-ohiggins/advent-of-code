from tutils import Any
from tutils import Callable
from tutils import List
from tutils import Tuple
from tutils import cast

from tutils import concat
from tutils import reduce

from tutils import lmap
from tutils import splitstriplines

from tutils import load_and_process_input
from tutils import run_tests


""" END HELPER FUNCTIONS """

Coords = Tuple[int, int]
CoordsPair = Tuple[Coords, Coords]


DAY = "06"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = None
TA2 = None
ANSWER1 = 400410
ANSWER2 = 15343601


def process_one(data: List[str]) -> int:
    def reducer(grid: List, line: str) -> List:
        coords, command = parse_command(line)
        return change_area(alter, grid, coords, command)

    lights = [[0] * 1000 for i in range(0, 1000)]

    return sum(concat(reduce(reducer, data, lights)))


def parse_command(text: str) -> Tuple[CoordsPair, str]:
    stripped = text.replace("turn ", "").strip()
    command, area = stripped.split(" ", 1)
    coords = get_coords(area)
    return (coords, command)


def get_coords(text: str) -> CoordsPair:
    start, end = text.split(" through ")
    start_strings, end_strings = start.split(","), end.split(",")
    start_coords = (int(start_strings[0]), int(start_strings[1]))
    end_coords = (int(end_strings[0]), int(end_strings[1]))
    return start_coords, end_coords


def change_area(
    func: Callable, grid: List, coords: CoordsPair, command: str
) -> List:
    start, end = coords
    for j in range(start[1], end[1] + 1):
        for i in range(start[0], end[0] + 1):
            grid[j][i] = func(grid[j][i], command)
    return grid


def alter(current_value: int, command: str) -> int:
    new_values = {"on": 1, "off": 0, "toggle": int(not bool(current_value))}
    return new_values[command]


def process_two(data: Any) -> Any:
    def reducer(grid: List, command: str) -> List:
        return change_area(alter2, grid, *parse_command(command))

    lights = [[0] * 1000 for i in range(0, 1000)]

    return sum(concat(reduce(reducer, data, lights)))


def alter2(current_value: int, command: str) -> int:
    new_values = {
        "on": current_value + 1,
        "off": max([0, current_value - 1]),
        "toggle": current_value + 2,
    }
    return new_values[command]


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
--- Day 6: Probably a Fire Hazard ---

Because your neighbors keep defeating you in the holiday house decorating
contest year after year, you've decided to deploy one million lights in a
1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed
you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at
each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include
whether to turn on, turn off, or toggle various inclusive ranges given as
coordinate pairs. Each coordinate pair represents opposite corners of a
rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers
to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by
doing the instructions Santa sent you in order.

For example:

    turn on 0,0 through 999,999 would turn on (or leave on) every light.

    toggle 0,0 through 999,0 would toggle the first line of 1000 lights,
    turning off the ones that were on, and turning on the ones that were off.

    turn off 499,499 through 500,500 would turn off (or leave off) the middle
    four lights.

After following the instructions, how many lights are lit?

Your puzzle answer was 400410.
--- Part Two ---

You just finish implementing your winning light pattern when you realize you
mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each
light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness of
those lights by 1.

The phrase turn off actually means that you should decrease the brightness of
those lights by 1, to a minimum of zero.

The phrase toggle actually means that you should increase the brightness of
those lights by 2.

What is the total brightness of all lights combined after following Santa's
instructions?

For example:

    turn on 0,0 through 0,0 would increase the total brightness by 1.

    toggle 0,0 through 999,999 would increase the total brightness by 2000000.

Your puzzle answer was 15343601.
"""
