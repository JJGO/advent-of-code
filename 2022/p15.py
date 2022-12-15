import parse
import numpy as np
from numba import njit


def parses(input):
    template = "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}"
    return [parse.parse(template, line).fixed for line in input.strip().split("\n")]


def merge_intervals(intervals):
    merged_intervals = []
    for s, e in sorted(intervals):
        if not merged_intervals or s > merged_intervals[-1][1] + 1:
            merged_intervals.append([s, e])
        else:
            merged_intervals[-1][1] = max(merged_intervals[-1][1], e)
    return merged_intervals


def intervals_at_y(data, y):
    intervals = []
    for sx, sy, bx, by in data:
        r = abs(sx - bx) + abs(sy - by)
        ry = r - abs(sy - y)
        if ry >= 0:
            intervals.append([sx - ry, sx + ry])
    return merge_intervals(intervals)


def solve_a(data, y=2_000_000):
    intervals = intervals_at_y(data, y)
    beacons_y = len(set(bx for _, _, bx, by in data if by == y))
    return sum((e - s + 1) for s, e in intervals) - beacons_y


def solve_b_interval(data, bounds=4_000_000):
    # Do part1 for each possible y
    # Not too crazy of a runtime because of part1 efficiency
    for y in range(bounds + 1):
        intervals = intervals_at_y(data, y)
        for s, e in intervals:
            if s >= 0 and e <= bounds:
                return (s - 1) * 4_000_000 + y
            if e + 1 <= bounds:
                return (e + 1) * 4_000_000 + y
            if s > bounds:
                break


@njit
def solve_b_perimeter(data, bounds=4_000_000):
    # Since there is a single solution, this implies that
    # it must be right next to at least one of the
    # perimeters of the diamonds defined by the scanners
    # Fast if JITed, otherwise comparable to _interval method
    sensors = []
    for sx, sy, bx, by in data:
        r = abs(sx - bx) + abs(sy - by)
        sensors.append((sx, sy, r))

    for sx, sy, r in sensors:
        for x_sign, y_sign in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            R = r + 1
            for i in range(R):
                x, y = sx + R * x_sign - i, sy + y_sign * i
                if 0 <= x <= bounds and 0 <= y <= bounds:
                    for x2, y2, r2 in sensors:
                        if abs(x - x2) + abs(y - y2) <= r2:
                            break
                    else:
                        return x * 4_000_000 + y


def solve_b_smart(data, bounds=4_000_000):
    # As there is only one missing value, it's going to be just outside the
    # boundaries of at least two scanners (unless we're incredibly unlucky and it's
    # right on the bounds of the 0-4_000_000 square

    # Like the perimeter solution, the idea is to only test points at the diamond
    # perimeters. Even smarter than the perimeter solution is to only consider
    # points at the intersection of two line segments.

    # To simplify the logic, line segments can be simplified to lines since we
    # are going to do the scanner checks anyways. Computing intersection of
    # the two types of lines is trivial as it's a simple system of 2 eqs

    positive_offset = []  # y = x + b
    negative_offset = []  # y = -x + b
    scanners = []
    for sx, sy, bx, by in data:
        r = abs(sx - bx) + abs(sy - by)
        scanners.append((sx, sy, r))
        R = r + 1
        # lines that contain top of diamond (sx+R, sy)
        positive_offset.append(sy - sx - R)
        negative_offset.append(sy + sx + R)
        # lines that contain bottom of diamond (sx-R, sy)
        positive_offset.append(sy - sx + R)
        negative_offset.append(sy + sx - R)

    for pos in positive_offset:
        for neg in negative_offset:
            x, y = (neg - pos) // 2, (pos + neg) // 2
            if 0 <= x <= bounds and 0 <= y <= bounds:
                if all(abs(sx - x) + abs(sy - y) > r for sx, sy, r in scanners):
                    return x * 4_000_000 + y


def solve_b_smt(data, bounds=4_000_000):
    # We can just offload the hard work to a solver,
    # specifying the bounds as well as the fact that
    # the point we are looking for must like outside
    # ALL of the diamonds defined by the sensor-beacon
    # pairs. Runs in a similar amount of time to _interval
    import z3

    s = z3.Solver()
    x = z3.Int("x")
    y = z3.Int("y")
    for v in (x, y):
        s.add(0 <= v)
        s.add(v <= bounds)

    def manhattan(p1, p2):
        abs = lambda x: z3.If(x >= 0, x, -x)
        return sum(abs(x1 - x2) for x1, x2 in zip(p1, p2))

    for sx, sy, bx, by in data:
        r = abs(sx - bx) + abs(sy - by)
        s.add(manhattan((x, y), (sx, sy)) > r)
    if s.check():
        m = s.model()
        return m[x].as_long() * 4_000_000 + m[y].as_long()


sample = parses(
    """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=15)
    data = parses(puzzle.input_data)
    assert solve_a(sample, 10) == 26
    puzzle.answer_a = solve_a(data)
    assert solve_b_smart(sample, 20) == 56000011
    puzzle.answer_b = solve_b_smart(data)
