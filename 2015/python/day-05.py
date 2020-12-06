from collections import Counter
from pathlib import Path
from typing import Iterable
from toolz import compose_left, sliding_window  # type: ignore


IterableS = Iterable[str]
lfilter = compose_left(filter, list)  # lambda f, l: [*filter(f, l)]


def pick(keep: IterableS, d: dict) -> dict:
    return {k: d[k] for k in d if k in keep}


def not_bad(text):
    badseqs = ["ab", "cd", "pq", "xy"]
    for seq in badseqs:
        if seq in text:
            return False
    return True


def has_vowels(text):
    target = 3
    vowels = list("aeiou")
    ct = 0
    counted = Counter(text)
    for char in vowels:
        ct = ct + counted.get(char, 0)
    if ct >= target:
        return True
    return False


def consec(text):
    for i, char in enumerate(text):
        if i + 1 != len(text):
            if char == text[i + 1]:
                return True
    return False


def is_nice(text):
    return all([not_bad(text), has_vowels(text), consec(text)])


def twopair(text):
    pairs = list(sliding_window(2, text))
    spairs = [f"{_[0]}{_[1]}" for _ in pairs]
    counted = Counter(spairs)
    above_keys = [k for k in counted if counted[k] >= 2]
    above = pick(above_keys, counted)
    for k in above:
        first = text.find(k)
        if k in text[first + 2 :]:
            return True
    return False


def repeater(text):
    for triplet in sliding_window(3, text):
        if triplet[0] == triplet[2]:
            return True
    return False


def is_nice2(text):
    return all([twopair(text), repeater(text)])


if __name__ == "__main__":
    raw = Path("input-05.txt").read_text()
    raw = raw.strip()
    assert is_nice("ugknbfddgicrmopn")
    assert is_nice("aaa")
    assert not is_nice("jchzalrnumimnmhp")
    assert not is_nice("haegwjzuvuyypxyu")
    assert not is_nice("dvszwmarrgswjxmb")
    nice = lfilter(is_nice, raw.splitlines())
    print(len(nice))
    assert is_nice2("qjhvhtzxzqqjkmpb")
    assert is_nice2("xxyxx")
    assert not is_nice2("uurcxstgmygtbstg")
    assert not is_nice2("ieodomkazucvgmuy")
    nice2 = lfilter(is_nice2, raw.splitlines())
    print(len(nice2))


"""
--- Day 5: Doesn't He Have Intern-Elves For This? ---

Santa needs help figuring out which strings in his text file are naughty or
nice.

A nice string is one with all of the following properties:

    It contains at least three vowels (aeiou only), like aei, xazegov, or
    aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx,
    abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of
    one of the other requirements.

For example:

    ugknbfddgicrmopn is nice because it has at least three vowels
    (u...i...o...), a double letter (...dd...), and none of the disallowed
    substrings.
    aaa is nice because it has at least three vowels and a double letter, even
    though the letters used by different rules overlap.
    jchzalrnumimnmhp is naughty because it has no double letter.
    haegwjzuvuyypxyu is naughty because it contains the string xy.
    dvszwmarrgswjxmb is naughty because it contains only one vowel.

How many strings are nice?

Your puzzle answer was 258.

--- Part Two ---

Realizing the error of his ways, Santa has switched to a better model of
determining whether a string is naughty or nice. None of the old rules apply,
as they are all clearly ridiculous.

Now, a nice string is one with all of the following properties:

    It contains a pair of any two letters that appears at least twice in the
    string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like
    aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter
    between them, like xyx, abcdefeghi (efe), or even aaa.

For example:

    qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and
    a letter that repeats with exactly one letter between them (zxz).
    xxyxx is nice because it has a pair that appears twice and a letter that
    repeats with one between, even though the letters used by each rule
    overlap.
    uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a
    single letter between them.
    ieodomkazucvgmuy is naughty because it has a repeating letter with one
    between (odo), but no pair that appears twice.

How many strings are nice under these new rules?

Your puzzle answer was 53.
"""
