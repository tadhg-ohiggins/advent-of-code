from operator import add
from string import ascii_lowercase, ascii_uppercase
from more_itertools import chunked, divide
from toolz import compose_left, curry
from toolz.curried import flip
from tutils import c_lmap as cmap, splitstriplines
from tadhg_utils import star

TEST_ANSWERS = (157, 70)
PUZZLE_ANSWERS = (8053, 2425)

chunk = compose_left(
    flip(chunked)(3),  # Split into groups of 3.
    list,
)

letterscore = compose_left(
    (ascii_lowercase + ascii_uppercase).index,
    curry(add)(1),
)

twosplit = compose_left(
    curry(divide)(2),  # Divide in half.
    cmap(list),
)

get_common = compose_left(
    cmap(set),
    star(set.intersection),  # Pass all to intersection.
    set.pop,
)

get_common_score_and_sum = compose_left(
    cmap(get_common),
    cmap(letterscore),
    sum,
)

# Functions expected by the puzzle runner below:

preprocess = splitstriplines

part_one = compose_left(
    cmap(twosplit),
    get_common_score_and_sum,
)

part_two = compose_left(
    chunk,
    get_common_score_and_sum,
)
