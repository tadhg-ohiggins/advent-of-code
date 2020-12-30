from math import prod
from functools import partial
from operator import itemgetter
from typing import (
    Any,
    List,
    Sequence,
    Tuple,
)
from tutils import (
    splitstrip,
    splitstriplines,
    load_and_process_input,
    run_tests,
)

DAY = "13"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = 295
TA2 = 1068781
ANSWER1 = 203
ANSWER2 = 905694340256752


def parse_input(lines: List[str]) -> Tuple[int, list]:
    return int(lines[0]), splitstrip(lines[1], sep=",")


def earliest(target: int, bus_id: int) -> Tuple[int, int]:
    timespan = range(target - bus_id, target + 1)
    noremainder = next(filter(lambda i: i % bus_id == 0, timespan))
    return (bus_id, bus_id + noremainder)


def process_one(target_values: Tuple[int, list]) -> Any:
    target, values = target_values
    busids = [int(_) for _ in values if _ != "x"]
    busid, ts = min(map(partial(earliest, target), busids), key=itemgetter(1))
    return busid * (ts - target)


def chinese_remainder(n: Sequence[int], a: Sequence[int]) -> int:
    """
    n is the sequence of numbers whose remainders you have when dividing the
    unknown number by.
    a is the sequence of remainders.
    So if you know that x % 3 = 2, x % 5 = 3, and x % 7 = 2, then:

        chinese_remainder([3, 5, 7], [2, 3, 2])

    will return 23.
    """
    product = prod(n)

    def step(num_remainder: Tuple[int, int]) -> int:
        number, remainder = num_remainder
        p = product // number
        return remainder * modular_inverse(p, number) * p

    return sum(map(step, zip(n, a))) % product


def extended_euclidean(x: int, y: int) -> Tuple[int, int, int]:
    """
    See:
    shainer.github.io/crypto/math/2017/10/22/chinese-remainder-theorem.html

    Given two integers, returns their greatest common denominator and
    the two coefficients in the Bézout identity.
    """
    x0, x1, y0, y1 = 1, 0, 0, 1

    while y > 0:
        q, x, y = x // y, y, x % y
        x0, x1 = x1, x0 - (q * x1)
        y0, y1 = y1, y0 - (q * y1)

    return x, x0, y0


def modular_inverse(factor: int, mod: int) -> int:
    """
    See:
    shainer.github.io/crypto/math/2017/10/22/chinese-remainder-theorem.html

    Solves for x in e.g. (17*x) % 43 = 1
    """
    q, x, _ = extended_euclidean(factor, mod)
    if q != 1:
        assert False
    return x % mod


def process_two(target_values: Tuple[int, list]) -> Any:
    _, values = target_values
    # The negative sign for i below is critical; otherwise we get much smaller
    # results than we want (and in fact would get a value that needed to be
    # subtracted from the product of all the factors to get the answer, instead
    # the answer itself).
    targets = [(int(item), -i) for i, item in enumerate(values) if item != "x"]
    numbers, offsets = zip(*targets)
    return chinese_remainder(numbers, offsets)


def cli_main() -> None:
    input_funcs = [splitstriplines, parse_input]
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
