from functools import partial, reduce
from itertools import cycle
from operator import add, sub, methodcaller, mul, truediv
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
replacer = lambda p, s, t: t.replace(p, s)
splitstrip = compose_left(str.split, lstrip, lcompact)
splitstriplines = compose_left(str.splitlines, lstrip, lcompact)
seq_to_dict = compose_left(lmap, dict)
split_to_dict = lambda s, **kwds: seq_to_dict(partial(splitstrip, **kwds), s)
c_map = curry(map)
c_lmap = curry(lmap)


def repladucer(pairs: List[Tuple[str, str]], text: str) -> str:
    # repladucer([("a", "1"), ("de", "DE"), ("f", "G")], "abcdef") -> "1bcDEG"
    return compose_left(*[partial(replacer, p, s) for p, s in pairs])(text)


def padder(chars: List[str], text, padstr=" "):
    # padder(["(", ")"], "some(parenthtical).") -> "some ( parenthetical ) ."
    return repladucer([(c, f"{padstr}{c}{padstr}") for c in chars], text)


def process_input(text):
    return lcompact(text.splitlines())


def load_input(fname):
    raw = Path(fname).read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    return raw


def process(data):
    return sum([teval_expr(line) for line in data])


def eval_base(expr: List[str]):
    print(expr)
    if len(expr) == 1:
        return expr[0]

    ops = {"+": add, "/": truediv, "*": mul, "-": sub}
    assertions = [
        expr[0] not in ops,
        expr[1] in ops,
        expr[2] not in ops,
    ]
    if not all(assertions):
        import pdb

        pdb.set_trace()
    assert all(assertions)
    left, operator, right = expr[:3]

    result = ops[operator](*lmap(int, [left, right]))
    return eval_base([result] + expr[3:])


def prep_expr(text):
    pad_parens = partial(padder, ["(", ")"])
    stripspacesplit = compose_left(lambda x: x.split(" "), lstrip, lcompact)
    return compose_left(pad_parens, stripspacesplit)(text)


def teval_expr(text):
    return compose_left(prep_expr, eval_expr)(text)


def eval_expr(items: List[str]):
    return eval_expr(cut_parens(items)) if "(" in items else eval_base(items)


def xsplit_at_last(array, func, keep_separator=False):
    # split_at_last([x, y, x, y, z], is_x) -> [[x, y], [y, z]]
    pieces = list(split_at(array, func, keep_separator=keep_separator))
    end = pieces[-1]
    start = list(concat(pieces[:-2]))
    if keep_separator:
        return [start, pieces[-2], end]
    return [start, end]


def split_at_last(array, func, keep_separator=False):
    pieces = list(
        split_at(array[::-1], func, keep_separator=keep_separator, maxsplit=1)
    )
    end = list(reversed(pieces[0]))
    start = list(concat(lmap(reversed, pieces[1:])))
    return [start, end]


def pairgrouper(pair: Sequence, array: List, func: Callable = list) -> List:
    # pairgouper([a, b, (, c, (, d, ), ),e, f]) -> [[a, b], [c, [d]], [e, f]]
    cycler = cycle(pair)
    while any([c in array for c in pair]):
        target = next(cycler)
        start, focus = split_at_last(array, lambda x: x == target)
        target = next(cycler)
        middle, end = split_at(focus, lambda x: x == target, maxsplit=1)
        array = start + [func(middle)] + end

    return array


cut_parens = lambda e, func=eval_expr: pairgrouper("()", e, func=func)


def xcut_parens(expr: List[str], func=eval_expr):
    if "(" not in expr:
        return expr
    cycler = cycle("()")
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
    """
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
    """
    try:
        sl = split_at_last([1, 2, 1, 3, 4], lambda x: x == 1)
        assert sl == [[1, 2], [3, 4]]
        sl2 = split_at_last(
            [1, 2, 1, 3, 4], lambda x: x == 1, keep_separator=True
        )
        assert sl2 == [[1, 2], [1], [3, 4]]
        sl3 = split_at_last([1, 2, 1, 3, 4, 1], lambda x: x == 1)
        assert sl3 == [[1, 2, 1, 3, 4], []]
        sl4 = split_at_last(
            [1, 2, 1, 3, 4, 1], lambda x: x == 1, keep_separator=True
        )
        assert sl4 == [[1, 2, 1, 3, 4], [1], []]
    except:

        import pdb

        pdb.set_trace()
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
    cli_main()
