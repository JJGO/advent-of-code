from collections import defaultdict
from heapq import heappop, heappush
import numpy as np


def parses(input):
    input = [list(line) for line in input.strip().split()]
    return input


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve(data, part):
    # precompute positions without blizzard at each timestep t
    # We decompose vertical and horizontal blizzards separately
    # so we don't have to deal with LCM(H,W) period but with
    # H and W separately. We store clear coordinates because
    # there is way more blizzard than empty points, so set will be
    # smaller
    directions = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
    inside = np.array(data)[1:-1, 1:-1]
    H, W = len(inside), len(inside[0])

    clear_cols = defaultdict(lambda: set(range(W)))  # index r, t
    clear_rows = defaultdict(lambda: set(range(H)))  # index c, t

    start = -1, data[0].index(".") - 1
    end = H, data[-1].index(".") - 1
    for i, c in enumerate("v^><"):
        winds_init = np.argwhere(inside == c)

        if i < 2:
            for t in range(H):
                for r, c in winds_init + t * directions[i]:
                    clear_rows[c, t].discard(r % H)
        else:
            for t in range(W):
                for r, c in winds_init + t * directions[i]:
                    clear_cols[r, t].discard(c % W)

    for r, c in (start, end):
        for t in range(W):
            clear_cols[r, t] = set([c])
        for t in range(H):
            clear_rows[c, t] |= set([r])
    clear_rows, clear_cols = dict(clear_rows), dict(clear_cols)

    # Perform A* three times
    #  Heuristic is just manhattan distance to destination
    # Important bit is to make sure that visited keeps track of (x,y,t) pairs
    # In the impl, we hash the entire state which is ok but only because
    # cost only depends on (x,y,t)
    # For this particular problem BFS with a queue also works well (only 2x slower)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]  # add no-op

    def fastest(start, end, offset):
        visited = set()

        heap = [(manhattan(start, end), start, 0)]

        while heap:
            cost, pos, t = heappop(heap)

            for d in directions:
                next_pos = add(pos, d)
                if next_pos == end:
                    return t + 1
                r, c = next_pos
                tr = (t + 1 + offset) % H
                tc = (t + 1 + offset) % W
                empty_row = (c, tr) in clear_rows and r in clear_rows[c, tr]
                empty_col = (r, tc) in clear_cols and c in clear_cols[r, tc]
                if empty_row and empty_col:
                    new_cost = t + 1 + manhattan(next_pos, end)
                    new_state = (new_cost, next_pos, t + 1)
                    if new_state not in visited:
                        visited.add(new_state)
                        heappush(heap, new_state)

    t1 = fastest(start, end, 0)
    if part == "a":
        return t1
    elif part == "b":
        t2 = fastest(end, start, t1)
        t3 = fastest(start, end, t1 + t2)

        return t1 + t2 + t3


def solve_a(data):
    return solve(data, "a")


def solve_b(data):
    return solve(data, "b")


sample = parses(
    """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=24)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 18
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 54
    puzzle.answer_b = solve_b(data)
