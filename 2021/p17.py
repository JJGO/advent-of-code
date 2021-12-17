import math
import parse
import itertools


def parses(text):
    return tuple([i.fixed[0] for i in parse.findall("{:d}", text)])


def triangular_in_interval(low, high):
    # Solve for (x*(x+1))/2 = triangular
    a = math.ceil((-1 + math.sqrt(1 + 8 * low)) / 2)
    b = math.floor((-1 + math.sqrt(1 + 8 * high)) / 2)
    return a == b


def sign(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


def valid_velocities(bounds):
    left, right, bottom, top = bounds
    vxs = range(1, right + 1)
    vys = range(10 * (top - bottom), bottom - 1, -1)
    ways = 0
    for vx, vy in itertools.product(vxs, vys):
        x, y = 0, 0
        # init = (vx, vy)
        local_maxy = 0
        while not ((x < left and vx == 0) or (x > right and vx > 0) or (y < bottom)):
            x = x + vx
            y = y + vy
            vx -= sign(vx)
            vy -= 1
            local_maxy = max(local_maxy, y)
            if left <= x <= right and bottom <= y <= top:
                yield local_maxy
                break
    return ways


def solve_a(bounds):
    left, right, bottom, _ = bounds
    if triangular_in_interval(left, right):
        # If we have a triangular number in ther interval
        # solution has clean close form
        y = 0 - bottom
        return y * (y - 1) // 2
    return next(valid_velocities(bounds))


def solve_b(bounds):
    return sum(1 for _ in valid_velocities(bounds))


sample = parses("target area: x=20..30, y=-10..-5")
tricky_sample = (42, 42, -10, -1)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=17)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 45
    assert solve_a(tricky_sample) == 3
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 112
    puzzle.answer_b = solve_b(data)
