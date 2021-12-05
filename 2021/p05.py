import parse
import itertools
from collections import defaultdict
import numpy as np


def parses(input):
    return [
        parse.parse("{:d},{:d} -> {:d},{:d}", line).fixed
        for line in input.strip().split("\n")
    ]


def overlap(points, part="a"):
    board = defaultdict(int)
    for x1, y1, x2, y2 in points:
        if (x1 == x2 or y1 == y2) or part == "b":
            if x1 < x2:
                xs = range(x1, x2 + 1)
            elif x1 > x2:
                xs = range(x1, x2 - 1, -1)
            else:
                xs = itertools.repeat(x1)
            if y1 < y2:
                ys = range(y1, y2 + 1)
            elif y1 > y2:
                ys = range(y1, y2 - 1, -1)
            else:
                ys = itertools.repeat(y1)
            for x, y in zip(xs, ys):
                board[x, y] += 1
    return sum(1 for v in board.values() if v > 1)


# Numpy flavored
def overlap_np(points, part="a"):
    points = np.array(points, dtype=np.int32)
    xmin, ymin = points.min(0).reshape(2, 2).min(0)
    xmax, ymax = points.max(0).reshape(2, 2).max(0)
    board = np.zeros(((xmax - xmin) + 1, (ymax - ymin) + 1))
    points -= np.array([[xmin, ymin, xmin, ymin]])
    for x1, y1, x2, y2 in points:
        if (x1 == x2 or y1 == y2) or part == "b":
            xs = np.arange(x1, x2+1) if x1 <= x2 else np.arange(x1, x2-1, -1)
            ys = np.arange(y1, y2+1) if y1 <= y2 else np.arange(y1, y2-1, -1)
            board[xs, ys] += 1
    return (board > 1).sum()


sample = parses(
    """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=5)
    data = parses(puzzle.input_data)
    for fn in (overlap, overlap_np):
        assert fn(sample, "a") == 5
        puzzle.answer_a = fn(data, "a")
        assert fn(sample, "b") == 12
        puzzle.answer_b = fn(data, "b")
