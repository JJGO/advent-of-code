import math
import re

import numpy as np


def parses(input):
    return [re.findall("\d+", line) for line in input.strip().split("\n")]


def solve(time, record):
    # simulate
    hold = np.arange(time + 1)
    dist = (time - hold) * hold
    return (dist > record).sum()


def solve(time, record):
    # quadratic formula
    #   x * (T-x) - R > 0
    #   -x**2 + Tx - R-1 >= 0
    #   x**2 - Tx + R+1 >= 0
    a, b, c = 1, -time, record + 1
    p, q = -b / (2 * a), (b ** 2 - 4 * a * c) ** 0.5 / (2 * a)
    x1, x2 = math.floor(p + q), math.ceil(p - q)
    return x1 - x2 + 1


def solve_a(data):
    return math.prod((solve(int(time), int(record))
                      for time, record in zip(*data)))


def solve_b(data):
    time, record = ["".join(vals) for vals in data]
    return solve(int(time), int(record))


sample = parses(
    """Time:      7  15   30
Distance:  9  40  200"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=6)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 288
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 71503
    puzzle.answer_b = solve_b(data)
