import itertools
from collections import Counter


def parses(input):
    return [x for x in input.strip().split("\n")]


def checksum(words):
    c2, c3 = 0, 0
    for w in words:
        c = Counter(w)
        c2 += any(i == 2 for i in c.values())
        c3 += any(i == 3 for i in c.values())
    return c2 * c3


def prototype(words):
    for a, b in itertools.combinations(words, 2):
        if sum(c != d for c, d in zip(a, b)) == 1:
            return "".join(c for c, d in zip(a, b) if c == d)


sampleA = [
    "abcdef",
    "bababc",
    "abbcde",
    "abcccd",
    "aabcdd",
    "abcdee",
    "ababab",
]

sampleB = [
    "abcde",
    "fghij",
    "klmno",
    "pqrst",
    "fguij",
    "axcye",
    "wvxyz",
]


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=2)
    data = parses(puzzle.input_data)

    assert checksum(sampleA) == 12
    puzzle.answer_a = checksum(data)
    assert prototype(sampleB) == "fgij"
    puzzle.answer_b = prototype(data)
