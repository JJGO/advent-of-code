from collections import Counter, deque
from sympy import zeros, eye


def parses(input):
    return [int(i) for i in input.split(",")]


def simulate(data, days):
    counts = Counter(data)
    population = deque([counts.get(i,0) for i in range(9)])
    for i in range(days):
        population.rotate(-1)
        population[6] += population[-1]
    return sum(population)


def fast_simulate(data, days):
    counts = zeros(9, 1)
    for i, v in Counter(data).items():
        counts[i, 0] += v

    transition = zeros(9, 9)
    transition[:-1, 1:] = eye(8)
    transition[6, 0] = transition[8, 0] = 1

    N = days
    while N > 0:
        N, r = divmod(N, 2)
        if r == 1:
            counts = transition @ counts
        transition = transition @ transition
    return int(sum(counts))


sample = parses("3,4,3,1,2")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=6)
    data = parses(puzzle.input_data)
    for fn in (simulate, fast_simulate):
        assert fn(sample, 18) == 26
        assert fn(sample, 80) == 5934
        puzzle.answer_a = fn(data, 80)

        assert fn(sample, 256) == 26984457539
        puzzle.answer_b = fn(data, 256)
