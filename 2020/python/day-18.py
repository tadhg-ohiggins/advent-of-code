from functools import partial, reduce
from operator import add, sub, mul, truediv
from pathlib import Path
from typing import (
    Any,
    Callable,
    List,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from more_itertools import split_at
from toolz import (  # type: ignore
    compose_left,
    concat,
    curry,
)


IterableS = Iterable[str]


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lcompact = partial(lfilter, None)
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lstrip = partial(lmap, str.strip)
splitstrip = compose_left(str.split, lstrip, lcompact)
splitstriplines = compose_left(str.splitlines, lstrip, lcompact)
seq_to_dict = compose_left(lmap, dict)
split_to_dict = lambda s, **kwds: seq_to_dict(partial(splitstrip, **kwds), s)
c_map = curry(map)
c_lmap = curry(lmap)


def process_input(text):
    return lcompact(text.splitlines())


def load_input(fname):
    raw = Path(fname).read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    return raw


def process(data):
    return sum([teval_expr(line) for line in data])


def eval_base(expr: List[str]):
    if len(expr) == 1:
        return expr[0]

    ops = {"+": add, "/": truediv, "*": mul, "-": sub}
    assert expr[0] not in ops
    assert expr[1] in ops
    assert expr[2] not in ops
    left = int(expr.pop(0))
    op = ops[expr.pop(0)]
    right = int(expr.pop(0))
    result = op(*[left, right])
    return eval_base([result] + expr)


def prep_expr(text):
    parened = text.replace("(", " ( ").replace(")", " ) ")
    return lcompact(parened.split(" "))


def teval_expr(text):
    elements = prep_expr(text)
    return eval_expr(elements)


def eval_expr(elements: List[str]):
    if "(" not in elements:
        return eval_base(elements)
    else:
        return eval_expr(cut_parens(elements))


def cut_parens(expr: List[str], func=eval_expr):
    if "(" not in expr:
        return expr
    opening, closing = None, None
    for i in range(len(expr))[::-1]:
        if expr[i] == "(":
            opening = i
            break

    for j, char in enumerate(expr[opening:]):
        if expr[j + opening] == ")":
            closing = opening + j
            break
    return (
        expr[:opening]
        + [func(expr[opening + 1 : closing])]
        + expr[closing + 1 :]
    )


def group_parens(expr: List[str]):
    if "(" not in expr:
        return expr
    return group_parens(cut_parens(expr, func=list))


def tests():
    xx = teval_expr("1 + 2")
    assert xx == 3
    yy = teval_expr("2 / 2")
    assert yy == 1
    zz = teval_expr("2 * 3")
    assert zz == 6
    ww = teval_expr("3 - 2")
    assert ww == 1
    xx = teval_expr("1 + 2 + 3")
    yy = teval_expr("(1 + 2 + 3)")
    zz = teval_expr("(1 + 2) + 3")
    assert xx == 6
    assert yy == 6

    x = "((4 * 6 * 3 + 5 * 6 + 9) + 4 * 7 + 2 + 5) + (3 * 6 + 4) + (7 + 8 + 8)"
    pe = prep_expr(x)
    gp = group_parens(pe)
    eval_adv(gp)
    ee = compose_left(prep_expr, group_parens, eval_adv)

    assert ee("1 + (2 * 3) + (4 * (5 + 6))") == 51
    xx = ee("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
    assert xx == 23340


def process_two(data):
    proc = compose_left(prep_expr, group_parens, eval_adv)
    return sum([proc(line) for line in data])


def eval_adv(expr: List):
    if all([isinstance(_, int) for _ in expr]):
        return reduce(mul, expr, 1)
    if any([isinstance(_, list) for _ in expr]):
        newels = []
        for el in expr:
            if isinstance(el, list):
                newels.append(eval_adv(el))
            else:
                newels.append(el)
        return eval_adv(newels)

    newvals = []
    for val in split_at(expr, lambda x: x == "*"):
        if "+" in val:
            newval = lfilter(lambda x: x != "+", val)
            newval = lmap(int, newval)
            newval = sum(newval)
            newvals.append([newval])
        else:
            newvals.append(lmap(int, val))

    return eval_adv(list(concat(newvals)))


def cli_main():
    data = compose_left(load_input, process_input)("input-18.txt")
    tests()
    answer = process(data)
    assert answer == 1451467526514
    print("Answer one:", answer)
    answer_two = process_two(data)
    assert answer_two == 224973686321527
    print("Answer two:", answer_two)


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer
    cli_main()
