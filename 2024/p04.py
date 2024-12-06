import itertools


def parses(input):
    return input.strip().split("\n")


def solve_a(data):
    total = 0
    N, M = len(data), len(data[0])
    for i in range(N):
        for j in range(M):
            for di, dj in itertools.product([-1, 0, 1], repeat=2):
                s = ""
                for k in range(len("XMAS")):
                    i2, j2 = i + di * k, j + dj * k
                    if 0 <= i2 < N and 0 <= j2 < M:
                        s += data[i2][j2]
                if s == "XMAS":
                    total += 1
    return total


def solve_b_other(data):
    total = 0
    N, M = len(data), len(data[0])
    for i in range(N):
        for j in range(M):
            for di, dj in itertools.product([-1, 1], repeat=2):
                s = ""
                for k in range(len("MAS")):
                    i2, j2 = i + di * k, j + dj * k
                    if 0 <= i2 < N and 0 <= j2 < M:
                        s += data[i2][j2]
                if s == "MAS":
                    if set([data[i + 2 * di][j], data[i][j + 2 * dj]]) == set("MS"):
                        total += 1

    return total // 2


def solve_b(data):
    total = 0
    N, M = len(data), len(data[0])
    for i in range(1, N - 1):
        for j in range(1, M - 1):
            if data[i][j] != "A":
                continue

            cs = [
                data[i + di][j + dj] for di, dj in itertools.product([-1, 1], repeat=2)
            ]
            if sorted(cs) != list("MMSS"):
                continue

            # diagonal is right if chars are the same
            # only need to check one diagonal
            if data[i - 1][j - 1] == data[i + 1][j + 1]:
                continue

            total += 1

    return total


sample = parses(
    """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=4)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 18
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 9
    puzzle.answer_b = solve_b(data)
