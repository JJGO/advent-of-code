import parse
import numpy as np


def parses(input):
    return [
        parse.parse("position=<{:d}, {:d}> velocity=<{:d}, {:d}>", line).fixed
        for line in input.strip().replace("  ", " ").replace("< ", "<").split("\n")
    ]


def sky(coords):
    # Linear system of equations (one pair of equations per point)
    # x + vx * t = Fx
    # y + vy * t = Fy
    # Solve for t, Fx, Fy
    # Fx, Fy are coords of intersection
    x, y, vx, vy = np.array(coords).T
    N = len(coords)
    B = np.concatenate((x, y)).reshape((2 * N, 1))
    A = np.zeros((2 * N, 3))
    A[:N, 0] = -vx
    A[N:, 0] = -vy
    A[N:, 2] = 1
    A[:N, 1] = 1
    sols, *_ = np.linalg.lstsq(A, B, rcond=None)
    t = int(round(sols[0, 0]))
    # Print
    x = x + t * vx
    y = y + t * vy
    xmin, xmax = x.min(), x.max() + 1
    ymin, ymax = y.min(), y.max() + 1
    sky = np.zeros((xmax - xmin, ymax - ymin))
    sky[x - xmin, y - ymin] = 1
    print("\n".join("".join(["#" if i else " " for i in line]) for line in sky.T))
    return t


sample = parses(
    """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""
)

if __name__ == "__main__":

    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=10)
    data = parses(puzzle.input_data)
    assert sky(sample) == 3

    sky(data)
    puzzle.answer_a = "RPNNXFZR"
    puzzle.answer_b = 10946
