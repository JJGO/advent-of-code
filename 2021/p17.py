import parse
import itertools


def parses(text):
    return tuple([i.fixed[0] for i in parse.findall("{:d}", text)])


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
    vys = range(abs(bottom), bottom - 1, -1)
    for vx, vy in itertools.product(vxs, vys):
        x, y = 0, 0
        init = (vx, vy)
        local_maxy = 0
        while not ((x < left and vx == 0) or (x > right and vx > 0) or (y < bottom)):
            x = x + vx
            y = y + vy
            vx -= sign(vx)
            vy -= 1
            local_maxy = max(local_maxy, y)
            if left <= x <= right and bottom <= y <= top:
                yield (init, local_maxy)
                break


# There's a heuristic of assuming that the process ends with
# vx = 0 and vy = bottom, so initial_vy = -bottom and
# max_height = (bottom)*(bottom+1)/2 due to the triangular sum
#
# However, while that heuristic works for the sample input,
# it requires some conditions to be met.
# For the heuristic to work, the [left, right] interval must
# contain a triangular number, otherwise we cannot reach vx=0,
# but a valid solution can still exist e.g. f(42,42,-10,-1) = 3
def solve_a(bounds):
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
