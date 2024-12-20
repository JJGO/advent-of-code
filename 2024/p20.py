import itertools


def parses(data):
    lines = data.strip().split("\n")
    start, end, walls = None, None, set()
    for i, row in enumerate(lines):
        for j, val in enumerate(row):
            if val == "#":
                walls.add((i, j))
            elif val == "S":
                assert start is None
                start = (i, j)
            elif val == "E":
                assert end is None
                end = (i, j)
    return start, end, walls


def compute_cost(data):
    start, end, walls = data
    pos = start
    cost = {start: 0}

    while pos != end:
        for delta in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            newpos = (pos[0] + delta[0], pos[1] + delta[1])
            if newpos not in walls and newpos not in cost:
                cost[newpos] = cost[pos] + 1
                pos = newpos
                break
    return cost


def solve_a(data, threshold=100):
    cost = compute_cost(data)
    shortcuts = {}
    for x, y in cost:
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            newpos = (x + dx, y + dy)
            if newpos in cost:
                shortcut = cost[newpos] - (cost[x,y] + 2)
                if shortcut > 0:
                    shortcuts[x, y, dx, dy] = shortcut
    return sum([1 for v in shortcuts.values() if v >= threshold])


def solve_b(data, threshold=100):
    cost = compute_cost(data)
    shortcuts = {}
    for a, b in itertools.combinations(cost, 2):
        dist = abs(a[0] - b[0]) + abs(a[1] - b[1])
        if dist <= 20:
            shortcut = cost[b] - (cost[a] + dist)
            shortcuts[a, b] = shortcut
    return sum([1 for v in shortcuts.values() if v >= threshold])


sample = parses(
    """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=20)
    data = parses(puzzle.input_data)
    assert solve_a(sample, threshold=40) == 2
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample, threshold=70) == 41
    puzzle.answer_b = solve_b(data)
