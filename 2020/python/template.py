from tutils import pdb
from tutils import subprocess
from tutils import Counter
from tutils import partial
from tutils import reduce
from tutils import wraps
from tutils import count
from tutils import groupby
from tutils import product
from tutils import prod
from tutils import itemgetter
from tutils import Path
from tutils import ascii_lowercase
from tutils import ascii_digits
from tutils import Any
from tutils import Callable
from tutils import List
from tutils import Iterable
from tutils import IterableS
from tutils import Optional
from tutils import Sequence
from tutils import OInt
from tutils import ODict
from tutils import UListStr
from tutils import Tuple
from tutils import Union
from tutils import hexc
from tutils import compose_left
from tutils import concat
from tutils import curry
from tutils import do
from tutils import excepts
from tutils import iterate
from tutils import keyfilter
from tutils import pluck
from tutils import pipe
from tutils import sliding_window
from tutils import toolz_pick
from tutils import toolz_omit
from tutils import omit
from tutils import pick
from tutils import add_debug
from tutils import add_debug_list
from tutils import run_process
from tutils import until_stable
from tutils import oxford
from tutils import excepts_wrap
from tutils import nextwhere
from tutils import noncontinuous
from tutils import lnoncontinuous
from tutils import lfilter
from tutils import lcompact
from tutils import lmap
from tutils import lpluck
from tutils import lstrip
from tutils import splitstrip
from tutils import splitstriplines
from tutils import seq_to_dict
from tutils import split_to_dict
from tutils import c_map
from tutils import c_lmap
from tutils import is_char_az
from tutils import is_char_hex
from tutils import is_char_az09
from tutils import filter_str
from tutils import filter_az
from tutils import filter_az09
from tutils import filter_hex
from tutils import add_pprint
from tutils import add_pprinting
from tutils import make_incrementer
from tutils import adjacent_transforms
from tutils import load_input
from tutils import process_input
from tutils import tests

from tutils import load_and_process_input
from tutils import run_tests


""" END HELPER FUNCTIONS """


DAY = "00"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = None
TA2 = None
ANSWER1 = None
ANSWER2 = None


def process_one(data: Any) -> Any:
    pdb.set_trace()
    return


def process_two(data: Any) -> Any:
    pdb.set_trace()
    return


def cli_main() -> None:
    input_funcs = [splitstriplines]
    data = load_and_process_input(INPUT, input_funcs)
    run_tests(TEST, TA1, TA2, ANSWER1, input_funcs, process_one, process_two)
    answer_one = process_one(data)
    if ANSWER1 is not None:
        if answer_one != ANSWER1:
            pdb.set_trace()

        assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    if ANSWER1 is not None:
        answer_two = process_two(data)
        if ANSWER2 is not None:
            if answer_two != ANSWER2:
                pdb.set_trace()
            assert answer_two == ANSWER2
        print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()
