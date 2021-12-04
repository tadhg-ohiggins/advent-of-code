import pdb
from functools import reduce
from operator import mul
import aoc
from tadhg_utils import splitstriplines, lmap, lconcat, lcompact, lfilter


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 4512
TA2 = 1924
A1 = 82440
A2 = None


def parse_input(data: str):
    sections = data.split("\n\n")
    numbers = sections[0].split(",")
    boards = sections[1:]
    lboards = lmap(splitstriplines, boards)
    dboards = lmap(lambda b: lmap(str.split, b), lboards)
    return (numbers, dboards)


def winner(board, number):
    numbers = lconcat(board)
    numbers = [n for n in numbers if not n.startswith("x")]
    total = sum(map(int, numbers))
    return total * int(number)


def change_board(number, board):
    rows = []
    for row in board:
        row = [n if n != number else f"x{n}" for n in row]
        rows.append(row)
    return rows


def check_for_winner(rows, number):
    cols = list(zip(*rows))
    if any(all(x.startswith("x") for x in row) for row in rows):
        return winner(rows, number)
    elif any(all(x.startswith("x") for x in col) for col in cols):
        return winner(rows, number)
    return None


def process_one(data):
    numbers, boards = data
    for number in numbers:
        boards = [change_board(number, board) for board in boards]
        for board in boards:
            if check_for_winner(board, number):
                return check_for_winner(board, number)

    pdb.set_trace()


def process_two(data):
    numbers, boards = data
    for number in numbers:
        boards = [change_board(number, board) for board in boards]
        if len(boards) == 1:
            if check_for_winner(boards[0], number):
                return check_for_winner(boards[0], number)
        else:
            boards = lfilter(lambda b: not check_for_winner(b, number), boards)


def cli_main() -> None:
    input_funcs = [parse_input]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    result_two = process_two(data)
    aoc.finish(result_one, A1, result_two, A2)


if __name__ == "__main__":
    cli_main()
