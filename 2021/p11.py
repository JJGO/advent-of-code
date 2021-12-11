import itertools
import numpy as np


def parses(input):
    return [[int(n) for n in line] for line in input.strip().split("\n")]


def run_step(energy):
    N, M = energy.shape
    energy += 1
    flashes = 0
    toflash = np.argwhere(energy > 9).tolist()
    while toflash:
        x, y = toflash.pop()
        flashes += 1
        for dx, dy in itertools.product([-1, 0, 1], repeat=2):
            x2, y2 = x + dx, y + dy
            if 0 <= x2 < N and 0 <= y2 < M and energy[x2, y2] < 10:
                energy[x2, y2] += 1
                if energy[x2, y2] == 10:
                    toflash.append([x2, y2])
    energy[energy > 9] = 0
    return flashes


def solve_a(energy, steps):
    energy = np.array(energy)
    return sum(run_step(energy) for k in range(steps))


def solve_b(energy):
    energy = np.array(energy)
    for k in itertools.count(1):
        run_step(energy)
        if (energy == 0).all():
            return k


sample = parses(
    """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=11)
    data = parses(puzzle.input_data)

    assert solve_a(sample, 10) == 204
    assert solve_a(sample, 100) == 1656
    puzzle.answer_a = solve_a(data, 100)

    assert solve_b(sample) == 195
    puzzle.answer_b = solve_b(data)
