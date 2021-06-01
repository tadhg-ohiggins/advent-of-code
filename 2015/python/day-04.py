import hashlib
from tutils import partial
from tutils import count
from tutils import Any
from tutils import compose_left


""" END HELPER FUNCTIONS """


DAY = "04"
INPUT, TEST = f"input-{DAY}.txt", f"test-input-{DAY}.txt"
TA1 = None
TA2 = None
ANSWER1 = 282749
ANSWER2 = 9962624


def process_one(data: str) -> int:
    return findzeroes(data, "00000")


def findzeroes(key, target):
    myhash = partial(mkhash, key)
    lazy_hashes = partial(map, myhash)
    find_match = partial(filter, lambda x: x[1].startswith(target))
    generator = compose_left(lazy_hashes, enumerate, find_match)(count())
    match = next(generator)
    return match[0]


def xfindzeroes(key, target):
    # This original is rather more readable than the functional version...
    i, hsh = 0, ""
    while not hsh.startswith(target):
        i = i + 1
        hsh = mkhash(key, i)
    return i


def mkhash(key, num):
    md5hash = hashlib.md5()
    md5hash.update(f"{key}{str(num)}".encode())
    return md5hash.hexdigest()


def process_two(data: Any) -> Any:
    return findzeroes(data, "000000")


def cli_main() -> None:
    data = "yzbqklnj"
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    answer_two = process_two(data)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()


"""
--- Day 4: The Ideal Stocking Stuffer ---

Santa needs help mining some AdventCoins (very similar to bitcoins) to use as
gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at
least five zeroes. The input to the MD5 hash is some secret key (your puzzle
input, given below) followed by a number in decimal. To mine AdventCoins, you
must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...)
that produces such a hash.

For example:

    If your secret key is abcdef, the answer is 609043, because the MD5 hash of
    abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest
    such number to do so.
    If your secret key is pqrstuv, the lowest number it combines with to make
    an MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of
    pqrstuv1048970 looks like 000006136ef....

Your puzzle answer was 282749.

--- Part Two ---

Now find one that starts with six zeroes.

Your puzzle answer was 9962624.
"""
