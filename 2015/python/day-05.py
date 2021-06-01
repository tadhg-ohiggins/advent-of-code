from tutils import Any
from tutils import Counter
from tutils import identity
from tutils import lfilter
from tutils import partitionby
from tutils import pick
from tutils import sliding_window
from tutils import splitstriplines
from tutils import valfilter

from tutils import load_and_process_input


""" END HELPER FUNCTIONS """


DAY = "05"
INPUT = f"input-{DAY}.txt"
ANSWER1 = 258
ANSWER2 = 53


def process_one(data: Any) -> Any:
    return len(lfilter(is_nice, data))


def is_nice(text: str) -> bool:
    return all([no_bad_seqs(text), has_enough_vowels(text), consec(text)])


def no_bad_seqs(text: str) -> bool:
    badseqs = ["ab", "cd", "pq", "xy"]
    return not any(seq in text for seq in badseqs)


def has_enough_vowels(text: str) -> bool:
    target = 3
    vowel_counts = pick("aeiou", Counter(text))
    return sum(vowel_counts.values()) >= target


def consec(text: str) -> bool:
    return any(len(_) > 1 for _ in partitionby(identity, text))


def process_two(data: str) -> int:
    return len(lfilter(is_nice2, data))


def is_nice2(text: str) -> bool:
    return all([twopair(text), repeater(text)])


def twopair(text: str) -> bool:
    pairs = map("".join, sliding_window(2, text))
    candidates = valfilter(lambda _: _ >= 2, Counter(pairs))
    # Make sure we're not including e.g. aaa as aa and aa:
    return any(k in text[text.find(k) + 2 :] for k in candidates)


def repeater(text: str) -> bool:
    return any(triplet[0] == triplet[2] for triplet in sliding_window(3, text))


def tests_one():
    assert is_nice("ugknbfddgicrmopn")
    assert is_nice("aaa")
    assert not is_nice("jchzalrnumimnmhp")
    assert not is_nice("haegwjzuvuyypxyu")
    assert not is_nice("dvszwmarrgswjxmb")


def tests_two():
    assert is_nice2("qjhvhtzxzqqjkmpb")
    assert is_nice2("xxyxx")
    assert not is_nice2("uurcxstgmygtbstg")
    assert not is_nice2("ieodomkazucvgmuy")


def cli_main() -> None:
    input_funcs = [splitstriplines]
    data = load_and_process_input(INPUT, input_funcs)
    tests_one()
    answer_one = process_one(data)
    assert answer_one == ANSWER1
    print("Answer one:", answer_one)
    tests_two()
    answer_two = process_two(data)
    assert answer_two == ANSWER2
    print("Answer two:", answer_two)


if __name__ == "__main__":
    cli_main()


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
