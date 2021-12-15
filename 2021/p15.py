from heapq import heappop, heappush


def parses(input):
    return [[int(i) for i in line] for line in input.strip().split("\n")]


class Cave:
    def __init__(self, data, part="a"):
        self.data = data
        N, M = len(data), len(data[0])
        self.N, self.M = N, M
        self.size = (N, M) if part == "a" else (5 * N, 5 * M)

    def __getitem__(self, pos):
        i, j = pos
        di, ri = divmod(i, self.N)
        dj, rj = divmod(j, self.M)
        risk = self.data[ri][rj] + di + dj
        risk = (risk - 1) % 9 + 1
        return risk


def search(cave):
    N, M = cave.size
    heap = [(0, (0, 0))]
    visited = set()
    while True:
        risk, (x, y) = heappop(heap)
        if (x, y) not in visited:
            if (x, y) == (N-1, M-1):
                return risk
            visited.add((x, y))
            for x2, y2 in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if 0 <= x2 < N and 0 <= y2 < M and (x2, y2) not in visited:
                    heappush(heap, (risk + cave[x2, y2], (x2, y2)))


def solve_a(data):
    return search(Cave(data, "a"))


def solve_b(data):
    return search(Cave(data, "b"))


sample = parses(
    """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=15)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 40
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 315
    puzzle.answer_b = solve_b(data)
