import itertools
from collections import defaultdict


def parses(data):
    data = data.strip().split("\n")
    N, M = len(data), len(data[0])

    antennas = defaultdict(list)
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            if v != ".":
                antennas[v].append((i + 1j * j))
    return (N, M), list(antennas.values())


def antinodes_a(locations, N, M):
    alocs = set()
    for a, b in itertools.combinations(locations, 2):
        locs = [a + (a-b), b - (a-b)]
        locs = [z for z in locs if (0 <= z.real < N) and (0 <= z.imag < M)]
        alocs |= set(locs)
    return alocs


def antinodes_b(locations, N, M):
    alocs = set()
    for a, b in itertools.combinations(locations, 2):
        for d in (a - b, b - a):
            z = a
            while (0 <= z.real < N) and (0 <= z.imag < M):
                alocs.add(z)
                z += d
    return alocs


def solve(data, antinodes):
    (N, M), grouped_dlocs = data
    all_locs = set()
    for locs in grouped_dlocs:
        all_locs |= antinodes(locs, N, M)
    return len(all_locs)


def solve_a(data):
    return solve(data, antinodes_a)


def solve_b(data):
    return solve(data, antinodes_b)


sample = parses("""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=8)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 14
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 34
    puzzle.answer_b = solve_b(data)
