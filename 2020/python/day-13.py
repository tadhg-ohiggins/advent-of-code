from functools import partial, reduce
from itertools import count
from math import lcm
from operator import itemgetter, mul
from pathlib import Path
from toolz import compose_left  # type: ignore


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lcompact = partial(lfilter, None)
splitstrip = compose_left(str.split, partial(lmap, str.strip), lcompact)


def earliest(target, num):
    for i in range(target - num, target + num + 1):
        if i % num == 0:
            if (target - i) < target:
                nearest = i + num
            return (num, nearest, i)


def testprocess():
    testinput = ["939", "7,13,x,x,59,x,31,19"]
    return process_one(testinput)


def testprocesstwo():
    testinput = ["939", "7,13,x,x,59,x,31,19"]
    return process_two(testinput)


def process_two(data, start=None, limit=None):

    blines = [int(_) if _ != "x" else _ for _ in data[1].split(",")]
    targets = [(item, i) for i, item in enumerate(blines) if item != "x"]
    lowest = lcm(*[_[0] for _ in targets])
    numbers = [_[0] for _ in targets]
    offsets = [_[1] for _ in targets]
    lcms = [x for x in targets if x[1] in numbers] + [targets[0]]
    steps = [lcm(*x) for x in lcms]
    realstepstest = [x for x in steps if (x != 0) and x % numbers[0] == 0]
    if realstepstest:
        realsteps = realstepstest[0]
        stepbase = realsteps / numbers[0]
        startoffset = [x for x in targets if x[0] == stepbase][0][1]
        reloffsets = [(x, i - startoffset) for x, i in targets]
    else:
        startoffset = 0
        stepbase = 1
        reloffsets = targets

    # pdb.set_trace()
    # startnum = 1 start if start else 1
    startnum = stepbase
    if start:
        startnum = start

    ctr = count(startnum, stepbase)
    print(stepbase)
    while True:
        i = next(ctr)
        conds = [((i + offset) % num) == 0 for num, offset in reloffsets]
        # print(conds)
        if all([((i + offset) % num) == 0 for num, offset in reloffsets]):
            return i - startoffset
        if limit:
            if i > limit:
                assert False


def p3(data):
    blines = [int(_) if _ != "x" else _ for _ in data[1].split(",")]
    targets = [(item, i) for i, item in enumerate(blines) if item != "x"]
    # lowest = lcm(*[_[0] for _ in targets])
    numbers = [_[0] for _ in targets]
    offsets = [_[1] for _ in targets]
    # total = reduce(mul, numbers, 1)
    subtract = chinese_remainder(numbers, offsets)
    mult = reduce(mul, numbers)
    # print(mult)
    # print(subtract)
    return mult - subtract
    """
    The above circuitous approach just happened to work; I had the remainders
    inverted here (if 13 departs one minute after 7, its remainder is -1, or
    12, not 1). With the above, if you multiply them all together and then
    subtract the chinese remainder theorem result with the reversed remainders,
    you get the same as if you just ran the theorem on the correct
    remainders.
    """
    running = 1
    # return total - subtract

    for target, offset in targets:
        running = (target - offset) * running
        print(running)
    return running  # - subtract


def process_one(data):
    target = int(data[0])
    nums = [int(_) for _ in data[1].split(",") if _ != "x"]
    bst = sorted([earliest(target, num) for num in nums], key=itemgetter(1))[0]
    return bst[0] * (bst[1] - target)


def chinese_remainder(n, a):

    total = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        total += a_i * mul_inv(p, n_i) * p
    return total % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def process(text):
    lines = lcompact(text.splitlines())
    testanswer = testprocess()
    assert testanswer == 295
    answer_one = process_one(lines)
    testanswertwo = testprocesstwo()
    examples = [
        # (["939", "7,13"], 1068781),
        (["939", "7,13,59"], 77),
        # (["939", "7,13,x,x,59,x,31,19"], 1068781),
        # (["939", "7,13,x,x,59,x,31,19"], 1068781),
        # (["", "17,x,13,19"], 3417),
        # (["", "67,x,7,59,61"], 779210),
        # (["", "67,7,x,59,61"], 1261476),
        # (["", "1789,37,47,1889"], 1202161486),
    ]
    for data, expected in []:
        print(data)
        if expected != 1202161486:
            # answer = process_two(data, limit=expected)
            answer = p3(data)

        else:
            answer = process_two(data, start=1202000000, limit=expected)
        print(answer)
        # assert answer == expected

    # a2 = process_two(lines)
    # a2 = process_two(lines, start=99999999986266)
    a3 = p3(examples[0][0])
    a2 = process_two(examples[0][0])
    a4 = p3(lines)
    print(a4)

    return


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer

    raw = Path("input-13.txt").read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    result = process(raw)
