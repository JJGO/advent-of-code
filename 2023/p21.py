import numpy as np


def parses(input):
    return [[".#S".index(c) for c in line] for line in input.strip().split("\n")]


# It's pretty much impossible to solve this without
# visualizing what's going on. The input is shaped
# in a diamond shape and the partB number is a
# 65 + 131N number with the map being 131x131 pixels
# Thus, you need to carefully count the number of
# even and odd panels


def as_coords(data):
    ROCK, START = 1, 2
    start = None
    rocks = []
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            pos = i + j * 1j
            if val == START:
                start = pos
            elif val == ROCK:
                rocks.append(pos)
    return start, set(rocks)


def solve_a(data, steps=64):
    start, rocks = as_coords(data)
    positions = set([start])
    for _ in range(steps):
        new_positions = set()
        for pos in positions:
            for delta in [1, -1, 1j, -1j]:
                if (new_pos := pos + delta) not in rocks:
                    new_positions.add(new_pos)
        positions = new_positions
    return len(positions)


def simulate_finite(data):
    N, M = len(data), len(data[0])
    start, rocks = as_coords(data)
    positions = set([start])
    for k in range(1, 132 + 1):
        new_positions = set()
        for pos in positions:
            for delta in [1, -1, 1j, -1j]:
                new_pos = pos + delta
                x, y = int(new_pos.real), int(new_pos.imag)
                if x < 0 or x >= N or y < 0 or y >= M:
                    continue
                if (x + 1j * y) not in rocks:
                    new_positions.add(new_pos)

        positions = new_positions

        if k == 131:
            full_odd = len(positions)
            deltas = [start - p for p in positions]
            outside_odd = sum((1 for z in deltas if abs(z.real) + abs(z.imag) > 65))
        if k == 132:
            full_even = len(positions)
            deltas = [start - p for p in positions]
            outside_even = sum((1 for z in deltas if abs(z.real) + abs(z.imag) > 65))

    return full_odd, outside_odd, full_even, outside_even


def solve_b_manual(data):
    full_odd, outside_odd, full_even, outside_even = simulate_finite(data)
    # This is highly convoluted and requires drawing
    # the square expressions are just cumulative sums of 4*n values
    # however since they alternate parity, it has to be split into two
    steps = 26501365
    n = (steps - 65) // 131
    assert (steps - 65) % 131 == 0 and n % 2 == 0
    corners = n * outside_even - (n + 1) * outside_odd
    inside = 4 * (n // 2) ** 2 * full_even + (2 * n // 2 + 1) ** 2 * full_odd
    return inside + corners


def simulate_infinite(data, steps):
    N, M = len(data), len(data[0])
    start, rocks = as_coords(data)
    positions = set([start])
    reachable = []
    for k in range(1, max(steps) + 1):
        new_positions = set()
        for pos in positions:
            for delta in [1, -1, 1j, -1j]:
                new_pos = pos + delta
                x, y = int(new_pos.real), int(new_pos.imag)
                if (x % N + 1j * (y % M)) not in rocks:
                    new_positions.add(new_pos)
        positions = new_positions

        if k in steps:
            reachable.append(len(positions))
    return reachable


def solve_b_polyfit(data):
    steps = steps = 26501365
    n = (steps - 65) // 131
    xs = np.arange(3)
    ys = simulate_infinite(data, 65 + 131 * xs)
    a, b, c = [int(round(k)) for k in np.polyfit(xs, ys, 2)]
    return a * n**2 + b * n + c


sample = parses(
    """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=21)
    data = parses(puzzle.input_data)
    assert solve_a(sample, 6) == 16
    puzzle.answer_a = solve_a(data)
    for solve_b in [solve_b_manual, solve_b_polyfit]:
        puzzle.answer_b = solve_b(data)
