from collections import Counter


def parses(input):
    return [
        (int(a), int(b))
        for line in input.strip().split("\n")
        for a, b in (line.split("   "),)
    ]


def solve_a(data):
    A, B = zip(*data)
    A = sorted(A)
    B = sorted(B)
    return sum(abs(a - b) for a, b in zip(A, B))


def solve_b(data):
    A, B = zip(*data)
    Cb = Counter(B)
    return sum(a * Cb[a] for a in A)


sample = parses(
    """3   4
4   3
2   5
1   3
3   9
3   3"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=1)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 11
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 31
    puzzle.answer_b = solve_b(data)
