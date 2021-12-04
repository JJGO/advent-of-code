import numpy as np


def parses(text):
    return np.array([int(i) for i in text.strip().split("\n")])


def count(depths):
    return (depths[1:] > depths[:-1]).sum()


def count_sliding(depths):
    # b + c + d > a + b + c iff d > a
    return (depths[3:] > depths[:-3]).sum()


sample = parses(
    """199
200
208
210
200
207
240
269
260
263"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=1)
    data = parses(puzzle.input_data)
    assert count(sample) == 7
    puzzle.answer_a = count(data)
    assert count_sliding(sample) == 5
    puzzle.answer_b = count_sliding(data)
