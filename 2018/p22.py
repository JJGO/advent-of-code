from enum import IntEnum
from heapq import heappush, heappop
import parse


def parses(text):
    depth, target = text.split("\n")
    depth = int(text.split()[1])
    target = parse.search("{:d},{:d}", target).fixed
    return depth, target


class Cave:
    def __init__(self, depth, target):
        self.depth = depth
        self._erosion = {}
        self.target = target

    def __getitem__(self, pos):
        if pos == self.target:  # or pos == (0,0):
            return 0
        return self.erosion(*pos) % 3

    def erosion(self, x, y):
        if (x, y) not in self._erosion:
            if y == 0:
                gi = x * 16807
            elif x == 0:
                gi = y * 48271
            else:
                gi = self.erosion(x - 1, y) * self.erosion(x, y - 1)
            self._erosion[x, y] = (gi + self.depth) % 20183
        return self._erosion[x, y]


def solve_a(data):
    depth, (H, W) = data
    cave = Cave(depth, (H, W))
    return sum(cave[i, j] for i in range(H + 1) for j in range(W + 1))


# Note if we let
# rocky=0, wet=1, narrow=2
# neither=0, torch=1, climbing=2
# then equipment is valid iff equip != region
def solve_b(data):
    depth, target = data
    X, Y = target
    cave = Cave(depth, target)
    torch = 1
    heap = [(X + Y, 0, (0, 0), torch)]
    visited = set()

    while True:
        # A* algorithm
        # Heap of heuristic, time, position, equipment
        C, T, (x, y), equip = heappop(heap)
        if (x, y, equip) in visited:
            continue
        if (x, y) == target and equip == torch:
            return T
        visited.add((x, y, equip))

        for equip2 in range(3):
            if equip2 != cave[x, y] and (x, y, equip2) not in visited:
                heappush(heap, (C + 7, T + 7, (x, y), equip2))

        for x2, y2 in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if (
                x2 >= 0
                and y2 >= 0
                and equip != cave[x2, y2]
                and (x2, y2, equip) not in visited
            ):
                C2 = T + 1 + abs(X - x2) + abs(Y - y2)
                heappush(heap, (C2, T + 1, (x2, y2), equip))


sample = parses(
    """depth: 510
target: 10,10"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=22)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 114
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 45
    puzzle.answer_b = solve_b(data)
