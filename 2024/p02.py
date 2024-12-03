def parses(input):
    return [[int(i) for i in line.split()] for line in input.strip().split("\n")]


def is_safe(seq):
    delta = [j - i for i, j in zip(seq, seq[1:])]
    return (all([i > 0 for i in delta]) or all([i < 0 for i in delta])) and all(
        [1 <= abs(i) <= 3 for i in delta]
    )


def is_almost_safe(seq):
    return is_safe(seq) or any(is_safe(seq[:i] + seq[i + 1 :]) for i in range(len(seq)))


def solve_a(data):
    return sum(is_safe(line) for line in data)


def solve_b(data):
    return sum(is_almost_safe(line) for line in data)


sample = parses(
    """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=2)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 2
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 4
    puzzle.answer_b = solve_b(data)
