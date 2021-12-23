import itertools
import parse
import numpy as np
from scipy.spatial.distance import cdist


def parses(data):
    pos = [i.fixed for i in parse.findall("{:d},{:d},{:d}", data)]
    r = [i.fixed[0] for i in parse.findall("r={:d}", data)]
    return np.array(pos), np.array(r)


def solve_a(data):
    pos, r = data
    i = np.argmax(r)
    distances = (abs(pos - pos[i])).sum(axis=1)
    return (distances <= r[i]).sum()


# Note about solutions to partB
# Afaik there's not a provably fast solution to this problem as you can find
# adversarial inputs to most strategies that lead to exponential runtime. See:
# https://ol.reddit.com/r/adventofcode/comments/a9co1u/day_23_part_2_adversarial_input_for_recursive/
# In particular, the problem can be reduced in polynomial time to MAX-CLIQUE
# which is in NP \intersection coNP (see Sipser p328) so all solutions should
# be exponential in the worst case.
# This is why the SMT solver strategy is not too outlandish for this problem


def solve_b_octree(data):
    # Fastest solution for given input, the "intended" solution by the creator (see Reddit)
    # This strategy starts with a big box representing all possible
    # points of interest, then it splits the box in 8 and keeps a heap of
    # (points_in_range, box) where boxes are ordered using distance to origin.
    # Once the popped box has measure zero it means that we are at a single point

    class Box:
        def __init__(self, low, high):
            self.low = np.array(low)
            self.high = np.array(high)

        def __repr__(self):
            return (
                f"{self.__class__.__name__}({self.low.tolist()}, {self.high.tolist()})"
            )

        def corners(self):
            return np.array(list(itertools.product(*zip(self.low, self.high))))

        def in_range(self, point, radius):
            return (abs(self.corners() - point).sum(1) <= radius).any()

        def count_in_range(self, points, radii):
            return (
                cdist(points, self.corners(), metric="cityblock").min(1) <= radii
            ).sum()

        def split(self):
            def _split(l, h):
                if l == h:
                    return [(l, l)]
                if l == h - 1:
                    return [(l, l), (h, h)]
                m = (l + h) // 2
                return [(l, m), (m, h)]

            splits = [_split(l, h) for l, h in zip(self.low, self.high)]
            return [Box(*zip(*s)) for s in itertools.product(*splits)]

        def measure(self):
            return (self.high - self.low).max()

        def __lt__(self, other):
            return abs(self.low).sum() < abs(other.low).sum()

    from heapq import heappush, heappop

    points, radii = data
    box = Box(points.min(0), points.max(0))
    heap = [(-box.count_in_range(points, radii), box)]

    while heap:
        _, box = heappop(heap)
        if box.measure() == 0:
            return box.low.sum()

        for child in box.split():
            in_range = child.count_in_range(points, radii)
            heappush(heap, (-in_range, child))


def solve_b_maxclique(data):
    import networkx as nx
    from networkx.algorithms.clique import find_cliques

    # 1. Computes graph of overlaps and searches for max-clique
    points, radii = data
    distances = cdist(points, points, metric="cityblock")
    max_dist = np.sum(np.meshgrid(radii, radii), axis=0)
    np.fill_diagonal(max_dist, -1)
    G = nx.Graph()
    for u, v in np.argwhere(distances <= max_dist):
        G.add_edge(u, v)
    max_clique = max(find_cliques(G), key=len)
    # 2. Given points in max_clique, it computes the maximum margin
    # (margin = distance-radius) of all points in the clique
    # This is because the closest point to the origin in the overlapping
    # region must be in the boundary of a point, we can sum directly
    margin = abs(points[max_clique]).sum(1) - radii[max_clique]
    return max(margin)


def solve_b_intervals(data):
    # Cheeky fast solution that does not find the point but just its magnitude.
    # Each point,radius can be encoded as an interval of magnitudes as
    # (L1(point)-r, L1(point)+r). We can compute the intersection of all
    # the intervals and if its non-empty the start of the interval is our solution

    # Since using all points is unfeasible, we can just try removing points and check
    # whether they get us closer to a feasible interval using a heap to ensure we
    # check the most promising interval
    from heapq import heappush, heappop

    points, radii = data
    lows, highs = abs(points).sum(1) - radii, abs(points).sum(1) + radii
    low, high = lows.max(), highs.min()
    violation = low - high
    if violation <= 0:
        return low
    heap = [(violation, list(range(len(points))))]
    while True:
        violation, i = heappop(heap)
        for n in i:
            j = i.copy()
            j.remove(n)
            low2, high2 = lows[j].max(), highs[j].min()
            violation2 = low2 - high2
            if violation2 <= 0:
                return low2
            heappush(heap, (violation2, j))


def solve_b_smtsolver(data):
    # Probably the slowest solution in runtime, but the easiest to implement
    # since it's just specifying it and letting Z3 solve
    from z3 import Int, If, Optimize, Sum

    points, radii = data
    points, radii = points.tolist(), radii.tolist()

    abs = lambda x: If(x >= 0, x, -x)

    def manhattan(p1, p2):
        return sum(abs(x1 - x2) for x1, x2 in zip(p1, p2))

    X = Int("x"), Int("y"), Int("z")

    opt = Optimize()

    total_inrange = Sum(
        [If(manhattan(X, p) <= r, 1, 0) for i, (p, r) in enumerate(zip(points, radii))]
    )
    origin_distance = manhattan(X, (0, 0, 0))
    c1 = opt.maximize(total_inrange)
    c2 = opt.minimize(origin_distance)
    if opt.check():
        return opt.lower(c2).as_long()


sample_a = parses(
    """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""
)

sample_b = parses(
    """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle
    import time

    puzzle = Puzzle(year=2018, day=23)
    data = parses(puzzle.input_data)

    assert solve_a(sample_a) == 7
    puzzle.answer_a = solve_a(data)

    for solve_b in [
        solve_b_octree,
        solve_b_intervals,
        solve_b_maxclique,
        solve_b_smtsolver,
    ]:
        assert solve_b(sample_b) == 36
        start = time.time()
        puzzle.answer_b = solve_b(data)
        print(solve_b.__name__, f"{time.time()-start:.2f}s")
