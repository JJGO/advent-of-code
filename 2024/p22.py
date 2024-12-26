import itertools


def parses(data):
    return [int(i) for i in data.strip().split("\n")]


def secrets(x):
    mask = (1 << 24) - 1
    while True:
        yield x
        x = (x ^ (x << 6)) & mask
        x = (x ^ (x >> 5)) & mask
        x = (x ^ (x << 11)) & mask


def solve_a(data):
    return sum((next(itertools.islice(secrets(secret), 2000, 2001)) for secret in data))


def prices(x):
    mask = (1 << 24) - 1
    nums = [x % 10]
    for _ in range(2000):
        x = (x ^ (x << 6)) & mask
        x = (x ^ (x >> 5)) & mask
        x = (x ^ (x << 11)) & mask
        nums.append(x % 10)
    return nums


def deltas(prices):
    d = [b - a for a, b in zip(prices, prices[1:])]
    deltas = {}
    for i, p in enumerate(prices[:-4]):
        seq = tuple(d[i : i + 4])
        if seq not in deltas:
            deltas[seq] = prices[i + 4]
    return deltas


def solve_b(data):
    total = {}
    for secret in data:
        for seq, p in deltas(prices(secret)).items():
            total[seq] = total.get(seq, 0) + p
    return max(total.values())


sample_a = parses(
    """1
10
100
2024"""
)

sample_b = parses("""1
2
3
2024""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=22)
    data = parses(puzzle.input_data)
    assert solve_a(sample_a) == 37327623
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample_b) == 23
    puzzle.answer_b = solve_b(data)
