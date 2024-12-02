import numpy as np


def parses(input):
    def parse_group(group):
        return [[".#".index(val) for val in row] for row in group.split("\n")]

    groups = input.strip().split("\n\n")
    return [parse_group(group) for group in groups]


def symmetries(data, smudge):
    total = 0
    for pattern in data:
        pattern = np.array(pattern, dtype=np.int8)
        for matrix, offset in [(pattern, 100), (pattern.T, 1)]:
            N = matrix.shape[0]
            for i in range(1, N):
                k = min(i, N - i)
                A = matrix[i - k : i]
                B = matrix[i : i + k][::-1]
                if abs(A - B).sum() == smudge:
                    total += offset * i
    return total


def solve_a(data):
    return symmetries(data, 0)


def solve_b(data):
    return symmetries(data, 1)


sample = parses(
    """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=13)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 405
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 400
    puzzle.answer_b = solve_b(data)
