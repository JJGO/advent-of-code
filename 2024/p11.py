from collections import Counter


def parses(data):
    return [int(i) for i in data.strip().split()]


def apply_rule(x):
    if x == 0:
        return [1]
    s = str(x)
    if len(s) % 2 == 0:
        n = len(s) // 2
        return [int(s[:n]), int(s[n:])]
    return [x * 2024]


def solve_a(data):
    nums = data
    for _ in range(25):
        nums = [m for n in nums for m in apply_rule(n)]
    return len(nums)


def solve_b(data):
    counts = Counter(data)
    for _ in range(75):
        new_counts = Counter()
        for n, c in counts.items():
            for m in apply_rule(n):
                new_counts[m] += c
        counts = new_counts
    return sum(counts.values())


sample = parses("""125 17""")

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=11)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 55312
    puzzle.answer_a = solve_a(data)
    puzzle.answer_b = solve_b(data)
