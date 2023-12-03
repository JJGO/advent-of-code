import itertools
import re
from math import prod


def parses(input):
    return input.strip().split("\n")


def solve_a(board):
    symbols = {
        (i, j)
        for i, row in enumerate(board)
        for j, val in enumerate(row)
        if val not in "0123456789."
    }

    total = 0
    for i, row in enumerate(board):
        for match in re.finditer("\d+", row):
            j, k = match.start(), match.end()
            for i2, j2 in itertools.product(range(i - 1, i + 2), range(j - 1, k + 1)):
                if (i2, j2) in symbols:
                    total += int(match.group())
                    break
    return total


def solve_b(board):

    gears = {
        (i, j): []
        for i, row in enumerate(board)
        for j, val in enumerate(row)
        if val == "*"
    }

    for i, row in enumerate(board):
        for match in re.finditer("\d+", row):
            j, k = match.start(), match.end()
            for i2, j2 in itertools.product(range(i - 1, i + 2), range(j - 1, k + 1)):
                if (i2, j2) in gears:
                    gears[i2, j2].append(int(match.group()))

    return sum(prod(parts) for gear, parts in gears.items() if len(parts) == 2)


sample = parses(
    """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=3)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 4361
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 467835
    puzzle.answer_b = solve_b(data)
