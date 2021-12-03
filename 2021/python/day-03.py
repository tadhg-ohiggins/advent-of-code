from collections import Counter
from functools import partial
import pdb
import aoc
from tadhg_utils import (
    c_lmap,
    lfilter,
    lmap,
    splitstriplines,
)


INPUT, TEST = aoc.get_inputs(__file__)
TA1 = 198
TA2 = 230
A1 = 749376
A2 = 2372923


def parse_lines_into_cols(data):
    ints = lmap(partial(lmap, int), data)
    crosswise = list(zip(*ints))
    return crosswise


def process_one(data):
    data = parse_lines_into_cols(data)
    gamma, epsilon = "", ""

    for column in data:
        gamma = gamma + str(Counter(column).most_common()[0][0])
        epsilon = epsilon + str(Counter(column).most_common()[-1][0])

    gamma_num = int(gamma, 2)
    epsilon_num = int(epsilon, 2)
    return gamma_num * epsilon_num


def process_two(data):
    cols = parse_lines_into_cols(data)
    oxy_lines = data[:]
    colnum = 0
    while len(oxy_lines) > 1:
        cols = parse_lines_into_cols(oxy_lines)
        most_common, mc_count = lmap(
            str, Counter(cols[colnum]).most_common()[0]
        )
        least_common, lc_count = lmap(
            str, Counter(cols[colnum]).most_common()[-1]
        )
        if mc_count == lc_count:
            most_common = "1"
        print(colnum, most_common, least_common, oxy_lines)
        oxy_lines = lfilter(lambda x: x[colnum] == most_common, oxy_lines)
        colnum = colnum + 1

    oxy_rating = int(oxy_lines[0], 2)

    co_lines = data[:]
    colnum = 0
    while len(co_lines) > 1:
        cols = parse_lines_into_cols(co_lines)
        most_common, mc_count = lmap(
            str, Counter(cols[colnum]).most_common()[0]
        )
        least_common, lc_count = lmap(
            str, Counter(cols[colnum]).most_common()[-1]
        )
        if mc_count == lc_count:
            least_common = "0"
        print(colnum, most_common, least_common, co_lines)
        co_lines = lfilter(lambda x: x[colnum] == least_common, co_lines)
        colnum = colnum + 1

    co_rating = int(co_lines[0], 2)

    return oxy_rating * co_rating


def cli_main() -> None:
    # Start: 2021-12-02 22:20
    input_funcs = [splitstriplines]
    data = aoc.load_and_process_input(INPUT, input_funcs)
    aoc.run_tests(TEST, TA1, TA2, A1, input_funcs, process_one, process_two)
    result_one = process_one(data)
    # 2021-12-02 22:31
    result_two = process_two(data)
    # 2021-12-02 23:03
    try:
        if A1 is not None:
            assert result_one == A1
        print("Answer one:", result_one)
        if A2 is not None:
            assert result_two == A2
        print("Answer two:", result_two)
    except AssertionError:
        pdb.set_trace()


if __name__ == "__main__":
    cli_main()
