from collections import defaultdict
import itertools
import parse


def parses(data):
    return [
        parse.parse("{}={:d}, {}={:d}..{:d}", line).fixed
        for line in data.strip().split("\n")
    ]


def fill(data):
    # Fully iterative solution
    scan = defaultdict(int)
    SAND, CLAY, WATER, RUNNING = 0, 1, 2, 3

    # Parse into map dictionary
    for a, n, b, m1, m2 in data:
        for m in range(m1, m2 + 1):
            if a == "x":
                scan[n, m] = CLAY
            else:
                scan[m, n] = CLAY

    # Start at prespecified source
    stack = [(500, 0)]
    ymax, ymin = max(y for x, y in scan), min(y for x, y in scan)

    while stack:
        x, y = stack.pop()
        scan[x, y] = RUNNING
        below = (x, y + 1)

        # Out of bounds or already explored
        if y >= ymax or scan[below] == RUNNING:
            continue

        # Continue downwards
        if scan[below] == SAND:
            stack.append(below)
            continue

        children = []
        filled = [(x, y)]
        still = True  # assume we'll hit a wall
        for side in (1, -1):
            for x2 in itertools.count(x + side, side):
                if scan[x2, y] == CLAY:
                    break  # Hit a wall
                scan[x2, y] = RUNNING
                filled.append((x2, y))

                below2 = (x2, y + 1)
                if scan[below2] == SAND:
                    children.append(below2)

                if scan[below2] in [SAND, RUNNING]:
                    still = False
                    break

        if still:
            for x2, y in filled:
                scan[x2, y] = WATER
            above = (x, y - 1)
            if scan[above] == RUNNING:
                stack.append(above)
        if children:
            # Keep in stack, but priotize children
            stack.append((x, y))
            stack.extend(children)
    sum_still = sum(1 for x, y in scan if scan[x, y] == WATER and ymin <= y <= ymax)
    sum_running = sum(1 for x, y in scan if scan[x, y] == RUNNING and ymin <= y <= ymax)
    return sum_still, sum_running


def solve_a(data):
    return sum(fill(data))


def solve_b(data):
    return fill(data)[0]


sample = parses(
    """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=17)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 57
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 29
    puzzle.answer_b = solve_b(data)
