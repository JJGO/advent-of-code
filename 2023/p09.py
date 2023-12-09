def parses(input):
    return [[int(i) for i in line.split(" ")] for line in input.strip().split("\n")]


def next_(seq):
    if all(n == 0 for n in seq):
        return 0
    diff = [b - a for a, b in zip(seq, seq[1:])]
    return seq[-1] + next_(diff)


def solve_a(data):
    return sum(next_(seq) for seq in data)


def solve_b(data):
    return sum(next_(seq[::-1]) for seq in data)


sample = parses(
    """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=9)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 114
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 2
    puzzle.answer_b = solve_b(data)
