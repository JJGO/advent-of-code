from numba import njit


def solve_a(steps, n=2017):
    d = {0: 0}
    p = 0
    for n in range(1, n + 1):
        for _ in range((steps + 1) % n):
            p = d[p]
        d[p], d[n] = n, d[p]
    return d[2017]


@njit
def solve_b(steps, n=50_000_000):
    after0 = 0
    p = 0
    for n in range(1, n + 1):
        p = (p + steps + 1) % n
        if p == 0:
            after0 = n
    return after0


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2017, day=17)
    data = int(puzzle.input_data)

    assert solve_a(3) == 638
    puzzle.answer_a = solve_a(data)
    puzzle.answer_b = solve_b(data)
