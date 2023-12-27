import itertools
import re

import numpy as np


def parses(input):
    def parse_line(line):
        nums = [int(i) for i in re.findall("-?\d+", line)]
        return (nums[:3], nums[3:])

    return [parse_line(line) for line in input.strip().split("\n")]


def intersect(p1, v1, p2, v2):
    ##### MATH
    # x = ox + vx * t
    # y = oy + vy * t

    # (x-ox)/vx = (y-oy)/vy

    # x/vx - y/vy = ox/vx - oy/vy
    # x/vx2 - y/vy2 = ox/vx2 - oy/vy2
    A = np.array(
        [
            [1 / v1[0], -1 / v1[1]],
            [1 / v2[0], -1 / v2[1]],
        ]
    )
    b = np.array(
        [
            [p1[0] / v1[0] - p1[1] / v1[1]],
            [p2[0] / v2[0] - p2[1] / v2[1]],
        ]
    )
    if np.linalg.det(A) == 0:
        return None, None
    return np.linalg.solve(A, b)


def solve_a(data, low=200000000000000, high=400000000000000):
    intersections = 0
    for (p1, v1), (p2, v2) in itertools.combinations(data, 2):
        x, y = intersect(p1, v1, p2, v2)
        if x is None:
            continue
        t1 = (x - p1[0]) / v1[0]
        t2 = (x - p2[0]) / v2[0]
        if t1 >= 0 and t2 >= 0:
            if low <= x <= high and low <= y <= high:
                intersections += 1

    return intersections


def solve_b(data):
    from z3 import Int, Solver

    solver = Solver()
    Px, Py, Pz = Int("Px"), Int("Py"), Int("Pz")
    Vx, Vy, Vz = Int("Vx"), Int("Vy"), Int("Vz")
    for i, ((px, py, pz), (vx, vy, vz)) in enumerate(data):
        t = Int(f"t{i}")
        solver.add(Px + Vx * t == px + vx * t)
        solver.add(Py + Vy * t == py + vy * t)
        solver.add(Pz + Vz * t == pz + vz * t)
        solver.add(t >= 0)
    assert str(solver.check()) == "sat"
    m = solver.model()
    val = m[Px].as_long() + m[Py].as_long() + m[Pz].as_long()
    return val


sample = parses(
    """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=24)
    data = parses(puzzle.input_data)
    assert solve_a(sample, 7, 27) == 2
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 47
    puzzle.answer_b = solve_b(data)
