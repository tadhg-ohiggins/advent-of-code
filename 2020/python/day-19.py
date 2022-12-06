import pdb
import re
import subprocess
from collections import Counter
from functools import partial, reduce, wraps
from itertools import count, groupby, product
from math import prod
from operator import add, itemgetter
from pathlib import Path
from pprint import pprint
from string import (
    ascii_lowercase,
    digits as ascii_digits,
)
import pyparsing as pp
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


from toolz import (  # type: ignore
    compose_left,
    concat,
    curry,
    do,
    excepts,
    iterate,
    juxt,
    keyfilter,
    keymap,
    pluck,
    pipe,
    sliding_window,
    valmap,
)

five = pp.Literal("b")
four = pp.Literal("a")
testc = pp.Combine(pp.Literal("a") + pp.Literal("b"))
three = pp.Or([pp.Combine(four + five), pp.Combine(five + four)])
two = pp.Or([pp.Combine(four + four), pp.Combine(five + five)])
one = pp.Or([pp.Combine(two + three), pp.Combine(three + two)])
root = pp.Combine(four + one + five)
# root = pp.Combine("a", "b", "a")


IterableS = Iterable[str]
hexc = ["a", "b", "c", "d", "e", "f"] + list(ascii_digits)


def toolz_pick(keep: IterableS, d: dict) -> dict:
    return keyfilter(lambda x: x in keep, d)


def toolz_omit(remove: IterableS, d: dict) -> dict:
    return keyfilter(lambda x: x not in remove, d)


def pick(keep: IterableS, d: dict) -> dict:
    return {k: d[k] for k in d if k in keep}


def omit(remove: IterableS, d: dict) -> dict:
    return {k: d[k] for k in d if k not in remove}


def add_debug(debug_f: Callable, orig_f: Callable) -> Callable:
    """
    Transforms the function such that output is passed
    to the debug function before being returned as normal.

    add_debug(print, str.upper) would return a function equivalent to:

    def fn(val: str): -> str
        result = str.upper(val)
        print(result)
        return result
    """
    do_f = partial(do, debug_f)
    return compose_left(orig_f, do_f)


def add_debug_list(debug_f: Callable, funcs: List[Callable]) -> List[Callable]:
    """
    Transforms each of the functions such that the output of each is passed
    to the debug function before being returned as normal.
    """
    return [add_debug(debug_f, f) for f in funcs]


def run_process(
    command: Union[list, str], options: Optional[dict] = None
) -> subprocess.CompletedProcess:
    base_opts = {"check": True, "text": True, "capture_output": True}
    opts = options if options else {}
    # pylint: disable=subprocess-run-check
    # return subprocess.run(command, **{**base_opts, **opts})  # type: ignore
    return subprocess.run(command, **(base_opts | opts))  # type: ignore


def until_stable(func: Callable) -> Callable:
    """
    Repeatedly call the same function on its arguments until the result doesn't
    change.

    Not sure how to make this work in variadic cases; comparing a single result
    to *args doesn't seem to work.
    """

    def inner(arg: Any, **kwds: Any) -> Any:
        if func(arg, **kwds) == arg:
            return arg
        return inner(func(arg, **kwds))

    return inner


def oxford(lst: List[str]) -> str:
    """
    Turns a list into a properly-formatted list phrase.
    ``["something"]`` becomes "something".
    ``["thing1", "thing2"]`` becomes "thing1 and thing2".
    ``["thing1", "thing2", "thing3"]`` becomes "thing1, thing2, and thing3".
    ``["a", "b", "c", "d"]`` becomes "a, b, c, and d".
    """
    if len(lst) <= 2:
        return " and ".join(lst)
    return f'{", ".join(lst[:-1])}, and {lst[-1]}'


def excepts_wrap(err: Any, err_func: Callable) -> Callable:
    """
    This basically means that::

        @excepts_wrap(ValueError, lambda _: None)
        def get_formatted_time(fmt: str, value: str) -> Optional[datetime]:
            return datetime.strptime(value.strip(), fmt)

        gft = get_formatted_time

    With the decorator, that's broadly equivalent to this without
    any decorator::

        gft = excepts(
            ValueError,
            get_formatted_time,
            lambda _: None
        )

    """

    def inner_excepts_wrap(fn: Callable) -> Callable:
        return excepts(err, fn, err_func)

    return inner_excepts_wrap


def firstwhere(pred: Callable, seq: Sequence) -> Any:
    return next(filter(pred, seq), False)


def noncontinuous(array: list[int]):
    """
    noncontinuous([1, 2, 3, 5, 6, 8, 9, 10]) == [[1, 2, 3], [5, 6], [8, 9, 10]]

    The difference between a number and its index will be stable for a
    consecutive run, so we can group by that.

    -1 for 1, 2, and 3; -2 for 5 and 6; -3 for 8, 9 and 10 in the above list.

    enumerate gets us item and index, a quick x[0] - x[1] lambda gets us the
    difference.

    Once we have them in groups, we extract them into the lists of runs.

    This could be all iterators instead of lists, but I'll make another
    function to do that translation.

    See also consecutive_groups in more_itertools, which was the basis for
    this.
    """
    check = lambda x: x[0] - x[1]
    collate = lambda x: map(itemgetter(1), list(x)[1])
    return map(collate, groupby(enumerate(array), key=check))


lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]
lcompact = partial(lfilter, None)
lmap = compose_left(map, list)  # lambda f, l: [*map(f, l)]
lpluck = compose_left(pluck, list)  # lambda k, l: [*pluck(f, l)]
lstrip = partial(lmap, str.strip)
splitstrip = compose_left(str.split, lstrip, lcompact)
splitstriplines = compose_left(str.splitlines, lstrip, lcompact)
seq_to_dict = compose_left(lmap, dict)
split_to_dict = lambda s, **kwds: seq_to_dict(partial(splitstrip, **kwds), s)
c_map = curry(map)
c_lmap = curry(lmap)
is_char_az = partial(
    lambda y, x: isinstance(x, str) and x in y, ascii_lowercase
)
is_char_hex = partial(lambda y, x: x in y, hexc)
is_char_az09 = partial(lambda y, x: x in y, ascii_lowercase + ascii_digits)
is_char_09 = partial(lambda y, x: x in y, ascii_digits)
filter_str = partial(lambda f, s: "".join(filter(f, s)))
filter_az = partial(filter_str, is_char_az)
filter_az09 = partial(filter_str, is_char_az09)
filter_09 = partial(filter_str, is_char_09)
filter_hex = partial(filter_str, is_char_hex)
add_pprint = partial(add_debug, pprint)
add_pprinting = partial(lmap, add_pprint)
make_incrementer = lambda start=0, step=1: partial(next, count(start, step))


def lnoncontinuous(array: list[int]):
    return lmap(list, noncontinuous(array))


def adjacent_transforms(
    dimensions: int, omit_origin: bool = True
) -> List[Tuple]:
    adj = product([-1, 0, 1], repeat=dimensions)
    not_origin = lambda x: not all([_ == 0 for _ in x])
    return lfilter(not_origin, adj) if omit_origin else adj


def process_input(text):
    rules, messages = splitstrip(text, "\n\n")
    return lmap(splitstriplines, [rules, messages])


def load_input(fname):
    raw = Path(fname).read_text()
    raw = raw.strip()  # comment this out if trailing stuff is important!
    return raw


def replace_in_val(pattern, sub, val):
    if pattern not in val.split():
        return val
    return " ".join(map(lambda x: sub if x == pattern else x, val.split()))


def combined_literals(array):
    return pp.Combine(reduce(add, [pp.Literal(_) for _ in array]))


def parse_rule(parsed, value):
    if all([is_char_az(c) for c in value.split()]):
        return combined_literals(splitstrip(value))
    if all([is_char_az(c) or c == "|" for c in splitstrip(value)]):
        left, right = [splitstrip(_) for _ in splitstrip(value, sep="|")]
        return pp.Or([combined_literals(left), combined_literals(right)])
    refs = compose_left(splitstrip, partial(lmap, filter_09), lcompact)(value)
    if not all([ref in parsed for ref in refs]):
        return None
    else:
        if "|" in value:
            left, right = splitstrip(value, sep="|")
            left, right = lmap(partial(parse_rule, parsed), [left, right])
            return pp.Or([left, right])
        else:
            newv = []
            for val in splitstrip(value):
                if val in parsed:
                    newv.append(parsed[val])
                elif is_char_az(val):
                    newv.append(pp.Literal(val))
                print(newv)
            return pp.Combine(reduce(add, newv))


def parse_rules(lines):
    """
    We want:
        { rulenum:
            {ordered: [ints],
            unordered: [ints]
        }
    """
    ruled = split_to_dict(lcompact(lines), sep=": ")
    ruled = valmap(lambda x: x.replace('"', ""), ruled)
    orig = {} | ruled

    while [x for x in ruled.values() if len(x.split()) == 1]:
        ones = [(x, y) for x, y in ruled.items() if len(y.split()) == 1]
        for key, value in ones:
            replace = partial(replace_in_val, key, value)
            ruled = valmap(replace, ruled)
            if key == "0":
                pdb.set_trace()
            del ruled[key]

    # while [x for x in omit(["0"], ruled).values() if len(x.split()) == 2]:
    twos = [(x, y) for x, y in ruled.items() if len(y.split()) == 2]
    for key, value in twos:
        rstr = r"\1(" + value + r")\2"
        print(rstr)
        replace = (
            lambda x: re.sub(
                # f"([ ^]+){key}([ $]+)", f"\1{value}\2", x
                f"(^|[ ]){key}([ ]|$)",
                rstr,
                x,
            )
            .replace("(", "")
            .replace(")", "")
        )
        ruled = valmap(replace, ruled)
        if key != "0":
            del ruled[key]

    parsed = {}
    count = 0
    while len(parsed) < len(ruled):
        for k in ruled:
            res = parse_rule(parsed, ruled[k])
            if res:
                parsed[k] = res

    missing = omit(parsed.keys(), ruled)
    return parsed
    """

    def to_int(text):
        print(text)
        if all([is_char_09(c) for c in text]):
            return int(text)
        else:
            print(text)
            return filter_az(text)

    def is_pairs(item):
        return all([isinstance(x, list) for x in item]) and len(item) == 2

    def ordering(text):
        options = splitstrip(text, "|")
        '''

        print(options)
        procs = compose_left(
            partial(lmap, splitstrip), partial(lmap, to_int), concat, list
        )
        return lmap(procs, options)
        '''
        print(options)
        a = lmap(splitstrip, options)
        print("a", a)
        b = lmap(partial(lmap, to_int), a)
        print("b", b)
        c = concat(b) if not is_pairs(b) else b
        print("c", c)
        d = list(c)
        print("d", d)
        return d

    func = compose_left(partial(keymap, int), partial(valmap, ordering))

    return func(ruled)
    """


is_all_az = lambda s: all([is_char_az(c) for c in s])


def resolve_rule(rules, resolved, key, rule):
    if len(rule) == 1:
        if is_all_az(rule[0]):
            resolved[key] = rule[0]
            return resolved
        if isinstance(rule[0], set):
            resolved[key] = rule[0]
            return resolved
        else:
            while any([isinstance(x, int) for x in rule[0]]):
                index, value = None, None
                for i, item in enumerate(rule[0]):
                    if not is_char_az(item):
                        if isinstance(item, int):
                            if item in resolved:
                                index = i
                                value = resolved[item]
                                break
                            else:
                                index = i
                                try:
                                    value = resolve_rule(
                                        rules, resolved, item, rules[item]
                                    )[item][0]
                                except:
                                    pdb.set_trace()
                                break
                        elif isinstance(item, set):
                            if item in resolved:
                                index = i
                                value = resolved[item]
                                break
                            else:
                                index = i
                                try:
                                    value = resolve_rule(
                                        rules, resolved, item, rules[item]
                                    )[item][0]
                                except:
                                    pdb.set_trace()
                                break
                rule[0][index] = value
                resolved[key] = rule
    else:
        xx = [x for y in rule for x in y]
        while any([isinstance(x, int) for y in rule for x in y]):

            for j, options in enumerate(rule):
                if is_all_az(options):
                    pass
                if isinstance(options, set):
                    pass
                else:
                    while any([isinstance(x, int) for x in options]):
                        index, value = None, None
                        for i, item in enumerate(options):
                            if not is_char_az(item):
                                if isinstance(item, int):
                                    if item in resolved:
                                        index = i
                                        value = resolved[item]
                                        break
                                    else:
                                        index = i
                                        try:
                                            value = resolve_rule(
                                                rules,
                                                resolved,
                                                item,
                                                rules[item],
                                            )[item][0]
                                        except:
                                            pdb.set_trace()
                                        break
                                elif isinstance(item, set):
                                    if item in resolved:
                                        index = i
                                        value = resolved[item]
                                        break
                                    else:
                                        index = i
                                        try:
                                            value = resolve_rule(
                                                rules,
                                                resolved,
                                                item,
                                                rules[item],
                                            )[item][0]
                                        except:
                                            pdb.set_trace()
                                        break
                        options[index] = value
                        rule[j] = options
                        resolved[key] = rule

        while any([isinstance(x, list) for y in rule for x in y]):

            pdb.set_trace()

    return resolved


def resolve_rules(rules):
    resolved = {}
    for k in sorted(rules.keys()):
        resolved = resolve_rule(rules, resolved, k, rules[k])

    return resolved


testdata = [
    "0: 4 1 5",
    "1: 2 3 | 3 2",
    "2: 4 4 | 5 5",
    "3: 4 5 | 5 4",
    '4: "a"',
    '5: "b"',
    "",
    "ababbb",
    "bababa",
    "abbbab",
    "aaabbb",
    "aaaabbb",
]


def tests():
    data = process_input("\n".join(testdata))
    rules = parse_rules(data[0])
    cfged = rules_to_cfg(rules)
    pdb.set_trace()
    # resolved = resolve_rules(rules)


def process(cfg, data):
    pdb.set_trace()
    return


def parse_rule_for_cfg(line):
    pdb.set_trace()


def rules_to_cfg(rules):
    order = sorted(rules.keys())[::-1]
    cfg = {}
    for k in order:
        cfg[k] = parse_rule_for_cfg(rules[k])


def cli_main():
    data = compose_left(load_input, process_input)("input-19.txt")
    pdb.set_trace()
    rules = parse_rules(data[0])
    # rules = parse_rules(data[0])
    # cfged = rules_to_cfg(rules)
    valid = 0
    for message in data[1]:
        try:
            xx = rules["0"].parseString(message)
            valid = valid + 1
        except:
            pass

    print(valid)
    pdb.set_trace()
    # answer = process(data)
    # pdb.set_trace()
    print("Answer one:", answer)


if __name__ == "__main__":
    # test = Path("test-input-00.txt").read_text().strip()
    # test_answer = whatever
    # assert process(test, params) == test_answer
    cli_main()
