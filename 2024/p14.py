import math
import numpy as np
from collections import Counter
import re


def parses(data):
    nums = [
        [int(i) for i in re.findall("-?\d+", line)] for line in data.strip().split("\n")
    ]
    nums = np.array(nums)
    return nums[:, :2], nums[:, 2:]


def solve_a(data, W=101, H=103):
    mod = np.array([W, H])
    pos, vel = data
    for _ in range(100):
        pos = (pos + vel) % mod
    w, h = W // 2, H // 2
    pos = pos[pos[:, 0] != w]
    pos = pos[pos[:, 1] != h]
    quads = Counter([(x // (w + 1), y // (h + 1)) for x, y in pos])
    return math.prod(quads.values())


def _render(pos, vel, n):
    mod = np.array([101, 103])
    best_pos = (pos + vel * n) % mod
    X = np.zeros(mod)
    for x, y in best_pos:
        X[x, y] = 1
    import matplotlib.pyplot as plt

    plt.imshow(X.T)
    plt.show()


def solve_b_var(data, plot=False):
    mod = np.array([101, 103])
    pos, vel = data

    when, best = 0, float("inf")
    # whole pattern must repeat every mod[0]*mod[1] steps
    for n in range(1, np.prod(mod)):
        pos = (pos + vel) % mod
        # heuristic for how spread out the points are
        std = pos.std(axis=0).sum()
        if std < best:
            best, when = std, n
    if plot:
        _render(pos, vel, when)

    return when


def solve_b_crt(data, plot=False):
    pos, vel = data
    Nx, Ny = 101, 103
    px, py = pos.T
    vx, vy = vel.T

    # Find most clustered time for each dimension independently
    all_px = (px[..., None] + np.arange(Nx) * vx[..., None]) % Nx
    all_py = (py[..., None] + np.arange(Ny) * vy[..., None]) % Ny
    bx = np.argmin(all_px.std(axis=0))
    by = np.argmin(all_py.std(axis=0))

    # Apply Chinese Remainder Theorem to find the time when both dimensions are clustered
    from sympy.ntheory.modular import crt

    b, _ = crt([Nx, Ny], [bx, by])
    if plot:
        _render(pos, vel, b)
    return b


sample = parses(
    """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=14)
    data = parses(puzzle.input_data)
    assert solve_a(sample, 11, 7) == 12
    puzzle.answer_a = solve_a(data)
    for solve_b in [solve_b_var, solve_b_crt]:
        puzzle.answer_b = solve_b(data)
