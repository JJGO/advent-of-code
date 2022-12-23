import itertools
from collections import Counter


def parses(input):
    return [
        (i, j)
        for i, line in enumerate(input.strip().split("\n"))
        for j, c in enumerate(line)
        if c == "#"
    ]


def simulate(data, steps):
    moves = [
        (-1, [-1, -1 + 1j, -1 - 1j]),
        (1, [1, 1 + 1j, 1 - 1j]),
        (-1j, [-1j, 1 - 1j, -1 - 1j]),
        (1j, [1j, 1 + 1j, -1 + 1j]),
    ]
    surroundings = set(sum([x for _, x in moves], start=[]))
    positions = {i + j * 1j for i, j in data}
    steps = range(steps) if steps else itertools.count()

    for n in steps:
        tentative = {}
        for p in positions:
            tentative[p] = p
            if all((p + dp) not in positions for dp in surroundings):
                continue
            for i in range(4):
                move, condition = moves[(n + i) % 4]
                if all((p + dp) not in positions for dp in condition):
                    tentative[p] = p + move
                    break

        counts = Counter(tentative.values())
        new_positions = {p2 if counts[p2] == 1 else p for p, p2 in tentative.items()}
        if positions == new_positions:
            return n + 1
        positions = new_positions

    return positions


def solve_a(data):
    positions = simulate(data, 10)
    sx = int(min(z.real for z in positions))
    ex = int(max(z.real for z in positions)) + 1
    sy = int(min(z.imag for z in positions))
    ey = int(max(z.imag for z in positions)) + 1
    return (ex - sx) * (ey - sy) - len(data)


def solve_b(data):
    return simulate(data, 0)


sample = parses(
    """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=23)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 110
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 20
    puzzle.answer_b = solve_b(data)
