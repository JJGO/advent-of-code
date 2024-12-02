import numpy as np
from scipy.spatial import distance
from scipy.spatial import ConvexHull


def parses(input):
    return [tuple(map(int, line.split(","))) for line in input.strip().split("\n")]


def findinternal(points):
    xpoints = np.array(points, dtype=np.int32)
    hull = ConvexHull(points=xpoints)
    maxH, maxW = xpoints.max(axis=0)
    minH, minW = xpoints.min(axis=0)
    xs = np.arange(minH, maxH + 1)
    ys = np.arange(minW, maxW + 1)
    zs = np.stack(np.meshgrid(xs, ys)).reshape(2, -1).T
    ds = distance.cdist(zs, points, metric="cityblock").astype(np.int32)
    ismin = ds == ds.min(1)[:, None]
    ismin = ismin[ismin.sum(1) == 1]  # points closest to single
    areas = ismin[ismin[:, hull.vertices].sum(1) == 0].sum(0)  # internal points
    return areas.max()


def safe(points, maxdist):
    xpoints = np.array(points)
    maxH, maxW = xpoints.max(axis=0) + maxdist // len(points)
    minH, minW = xpoints.min(axis=0) - maxdist // len(points)
    xs = np.arange(minH, maxH + 1)
    ys = np.arange(minW, maxW + 1)
    zs = np.stack(np.meshgrid(xs, ys)).reshape(2, -1).T
    ds = distance.cdist(zs, points, metric="cityblock").sum(axis=1)
    return (ds < maxdist).sum()


sample = parses(
    """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=6)
    data = parses(puzzle.input_data)
    assert findinternal(sample) == 17
    puzzle.answer_a = findinternal(data)
    assert safe(sample, 32) == 16
    puzzle.answer_b = safe(data, 10_000)
