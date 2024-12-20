def parses(data):
    lines = data.strip().split("\n")
    return {
        (i, j): int(n)
        for i, row in enumerate(lines)
        for j, n in enumerate(row)
        if n != "."
    }


def find_trails(start, board, unique):
    stack = [(*start, 0)]
    nines = set()
    trails = 0
    while stack:
        i, j, n = stack.pop()
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            i2, j2 = i + di, j + dj
            if (i2, j2) in board and board[i2, j2] == n + 1:
                if n == 8:
                    trails += (not unique) or ((i2, j2) not in nines)
                    nines.add((i2, j2))
                else:
                    stack.append((i2, j2, n + 1))
    return trails


def count_trails(board, unique):
    return sum(
        find_trails(start, board, unique) for start in board if board[start] == 0
    )


def solve_a(data):
    return count_trails(data, unique=True)


def solve_b(data):
    return count_trails(data, unique=False)


sample = parses(
    """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=10)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 36
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 81
    puzzle.answer_b = solve_b(data)
