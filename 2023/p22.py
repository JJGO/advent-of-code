import re
from collections import defaultdict
from functools import reduce

import numpy as np


def parses(input):
    def parse_line(line):
        nums = [int(i) for i in re.findall("-?\d+", line)]
        return (tuple(nums[:3]), tuple(nums[3:]))

    return [parse_line(line) for line in input.strip().split("\n")]


def build_graph(data):
    N, M, _ = [1 + reduce(max, [p[1][i] for p in data]) for i in range(3)]

    # sort by Z coordinate, then drop one at a time and update height map
    stack = sorted(data, key=lambda p: -p[0][2])
    heights = np.array([[0 for _ in range(M)] for _ in range(N)], dtype=np.int32)
    bricks = []
    by_height = defaultdict(list)  # makes building the above/below maps easier
    while stack:
        ((x0, y0, z0), (x1, y1, z1)) = stack.pop()
        h = 1 + heights[x0 : x1 + 1, y0 : y1 + 1].max()
        H = h + z1 - z0
        bricks.append(((x0, y0, h), (x1, y1, H)))
        heights[x0 : x1 + 1, y0 : y1 + 1] = H
        by_height[H].append(len(bricks) - 1)

    below = defaultdict(list)
    above = defaultdict(list)

    for i, p in enumerate(bricks):
        zmin = p[0][2]
        for candidate in by_height[zmin - 1]:
            inter = np.zeros_like(heights)
            (x0, y0, z0), (x1, y1, z1) = p
            (x2, y2, _), (x3, y3, _) = bricks[candidate]
            inter[x0 : x1 + 1, y0 : y1 + 1] += 1
            inter[x2 : x3 + 1, y2 : y3 + 1] += 1
            if inter.max() == 2:
                below[i].append(candidate)
                above[candidate].append(i)
    return bricks, below, above


def solve_a(data):
    bricks, below, above = build_graph(data)
    can_disintegrate = 0
    for i, _ in enumerate(bricks):
        for ontop in above[i]:
            if len(below[ontop]) == 1:
                break
        else:
            can_disintegrate += 1
    return can_disintegrate


def solve_b(data):
    bricks, below, above = build_graph(data)

    total = 0
    for k in range(len(bricks)):
        falling = set([k])
        for i in range(len(bricks)):
            supports = [b in falling for b in below[i]]
            if len(supports) > 0 and all(supports):
                falling.add(i)
        total += len(falling) - 1
    return total


sample = parses(
    """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=22)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 5
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 7
    puzzle.answer_b = solve_b(data)
