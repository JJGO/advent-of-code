from collections import deque


def parses(input):
    start = end = None
    elevation = []
    for i, line in enumerate(input.strip().split("\n")):
        elevation.append([])
        for j, c in enumerate(line):
            if c == "S":
                start = (i, j)
                c = "a"
            elif c == "E":
                end = (i, j)
                c = "z"
            elevation[-1].append(ord(c) - ord("a"))
    return elevation, start, end


def solve_a(data):
    elevation, start, end = data
    queue = deque([(*start, 0)])
    N, M = len(elevation), len(elevation[0])
    visited = set()
    while queue:
        i, j, steps = queue.popleft()
        if (i, j) == end:
            return steps
        for i2, j2 in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if 0 <= i2 < N and 0 <= j2 < M and (i2, j2) not in visited:
                if elevation[i2][j2] - elevation[i][j] <= 1:
                    visited.add((i2, j2))
                    queue.append((i2, j2, steps + 1))


def solve_b(data):
    elevation, start, end = data
    queue = deque([(*end, 0)])
    N, M = len(elevation), len(elevation[0])
    visited = set()
    while queue:
        i, j, steps = queue.popleft()
        if elevation[i][j] == 0:
            return steps
        for i2, j2 in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if 0 <= i2 < N and 0 <= j2 < M and (i2, j2) not in visited:
                if elevation[i][j] - elevation[i2][j2] <= 1:
                    visited.add((i2, j2))
                    queue.append((i2, j2, steps + 1))


sample = parses(
    """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=12)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 31
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 29
    puzzle.answer_b = solve_b(data)
