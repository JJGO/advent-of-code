import numpy as np
import parse
from numba import njit


def parses(input):
    data = [
        [parse.parse("{:d},{:d}", pair).fixed for pair in line.split(" -> ")]
        for line in input.strip().split("\n")
    ]
    cave = np.zeros((1000, 1000), dtype=np.uint8)
    for instructions in data:
        for (x1, y1), (x2, y2) in zip(instructions, instructions[1:]):
            if x1 == x2:
                cave[x1, min(y1, y2) : max(y1, y2) + 1] = 1
            elif y1 == y2:
                cave[min(x1, x2) : max(x1, x2) + 1, y1] = 1
            else:
                raise ValueError
    return cave


@njit
def simulate_sand(cave):
    EMPTY, ROCK, SAND = 0, 1, 2
    SRC = (500, 0)
    bottom = np.where(cave)[1].max()
    i = 0
    while cave[SRC] == 0:
        x, y = np.array(SRC)
        while cave[x, y] == EMPTY:
            i += 1
            if y + 1 > bottom:
                return (cave == SAND).sum()
            for x2, y2 in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
                if cave[x2, y2] == EMPTY:
                    x, y = x2, y2
                    break
            else:
                break
        cave[x, y] = SAND
    return (cave == SAND).sum()


def solve_a(cave):
    return simulate_sand(cave)


def solve_b(cave):
    bottom = 2 + np.where(cave)[1].max()
    cave[:, bottom] = 1
    return simulate_sand(cave)


sample = parses(
    """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=14)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 24
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 93
    puzzle.answer_b = solve_b(data)
