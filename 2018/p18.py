import itertools
import numpy as np


def parses(data):
    # 0=open, 1=trees, 2=lumber
    data = data.replace(".", "0").replace("|", "1").replace("#", "2")
    return [[int(i) for i in line] for line in data.strip().split("\n")]


def run_step(area):
    new_area = area.copy()
    neigh_slices = list(
        itertools.product([slice(None, -2), slice(1, -1), slice(2, None)], repeat=2)
    )
    neigh_slices.pop(4)  # Remove the center
    p_area = np.pad(area, 1, constant_values=0)
    neigh_trees = np.sum([p_area[s] == 1 for s in neigh_slices], axis=0)
    neigh_lumber = np.sum([p_area[s] == 2 for s in neigh_slices], axis=0)
    new_area[(area == 0) & (neigh_trees >= 3)] = 1
    new_area[(area == 1) & (neigh_lumber >= 3)] = 2
    new_area[(area == 2) & ((neigh_trees < 1) | (neigh_lumber < 1))] = 0
    return new_area


def solve_a(area, mins):
    area = np.array(area)
    for _ in range(mins):
        area = run_step(area)
    return (area == 1).sum() * (area == 2).sum()


def solve_b(area):
    seen = {}
    area = np.array(area)
    for k in itertools.count():
        area = run_step(area)

        h = hash("|".join("".join([str(c) for c in line]) for line in area))
        if h in seen:
            cycle_len = k - seen[h][0]
            mod_min = (1_000_000_000 - k - 1) % cycle_len
            return solve_a(area, mod_min)
        value = (area == 1).sum() * (area == 2).sum()
        seen[h] = (k, value)


sample = parses(
    """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=18)
    data = parses(puzzle.input_data)

    assert solve_a(sample, 10) == 1147
    puzzle.answer_a = solve_a(data, 10)
    puzzle.answer_b = solve_b(data)
