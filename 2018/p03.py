from parse import parse
import numpy as np


def parses(input):
    return [
        parse("#{} @ {:d},{:d}: {:d}x{:d}", line).fixed[1:]
        for line in input.strip().split("\n")
    ]


def overlaps(claims):
    fabric = np.zeros((1000, 1000))
    for i, j, x, y in claims:
        fabric[i : i + x, j : j + y] += 1
    return (fabric > 1).sum()


def no_overlap(claims):
    fabric = np.zeros((1000, 1000))
    for i, j, x, y in claims:
        fabric[i : i + x, j : j + y] += 1
    for k, (i, j, x, y) in enumerate(claims):
        if (fabric[i : i + x, j : j + y] > 1).sum() == 0:
            return k + 1


sample = parses(
    """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=3)
    data = parses(puzzle.input_data)
    assert overlaps(sample) == 4
    puzzle.answer_a = overlaps(data)
    assert no_overlap(sample) == 3
    puzzle.answer_b = no_overlap(data)
