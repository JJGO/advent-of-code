import math


def parses(input):
    return [[int(i) for i in line] for line in input.strip().split("\n")]


def solve_a(heights):
    N, M = len(heights), len(heights[0])
    total = 0
    for i in range(N):
        for j in range(M):
            h = heights[i][j]
            for i2, j2 in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
                if 0 <= i2 < N and 0 <= j2 < M:
                    if heights[i2][j2] <= h:
                        break
            else:
                total += 1 + h
    return total


# Classic number of islands, dfs on the implicit graph
# We know all basins are surrounded by 9s since problem states
# "...all other locations will always be part of exactly one basin."
def solve_b(heights):
    N, M = len(heights), len(heights[0])
    visited = set()
    basins = []

    for i in range(N):
        for j in range(M):
            if heights[i][j] != 9 and (i, j) not in visited:
                stack = [(i, j)]
                visited.add((i, j))
                basins.append(0)

                # DFS
                while stack:
                    x, y = stack.pop()
                    basins[-1] += 1
                    for x2, y2 in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                        if 0 <= x2 < N and 0 <= y2 < M:
                            if heights[x2][y2] != 9 and (x2, y2) not in visited:
                                visited.add((x2, y2))
                                stack.append((x2, y2))

    return math.prod(sorted(basins)[-3:])


sample = parses(
    """2199943210
3987894921
9856789892
8767896789
9899965678"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=9)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 15
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 1134
    puzzle.answer_b = solve_b(data)
