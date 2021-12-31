from collections import defaultdict


def parses(text):
    data = text.strip().split("\n")
    N, M = len(data), len(data[0])
    return [
        (i - M // 2, j - N // 2)
        for j, row in enumerate(data)
        for i, v in enumerate(row)
        if v == "#"
    ]


def solve_a(data, steps=10_000):
    infected = set(i + 1j * j for i, j in data)
    infections = 0
    pos = 0
    direction = -1j
    for _ in range(steps):
        if pos in infected:
            direction *= 1j
            infected.remove(pos)
        else:
            direction *= -1j
            infected.add(pos)
            infections += 1
        pos += direction
    return infections


def solve_b(data, steps=10_000_000):
    CLEAN, WEAK, INFECT, FLAG = 0, 1, 2, 3
    state = defaultdict(int)
    state.update({i + 1j * j: INFECT for i, j in data})
    infections = 0
    pos = 0
    direction = -1j
    for _ in range(steps):
        direction *= [-1j, 1, 1j, -1][state[pos]]
        infections += state[pos] == WEAK
        state[pos] = (state[pos] + 1) % 4
        pos += direction
    return infections


sample = parses(
    """..#
#..
..."""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2017, day=22)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 5587
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 2511944
    puzzle.answer_b = solve_b(data)
