from collections import defaultdict
import numpy as np
from scipy.spatial.distance import cdist


def parses(data):
    return np.array([[int(i) for i in line.split(',')] for line in data.strip().split('\n')])


def constellations(stars):
    distances = cdist(stars, stars, metric='cityblock')
    graph = defaultdict(list)
    for i, j in np.argwhere(distances <= 3):
        if i != j:
            graph[i].append(j)
    constellations = 0
    visited = set()
    for n, _ in enumerate(stars):
        if n not in visited:
            visited.add(n)
            constellations += 1
            stack = [n]
            while stack:
                m = stack.pop()
                for child in graph[m]:
                    if child not in visited:
                        visited.add(child)
                        stack.append(child)
    return constellations


samples = [
(parses(""" 0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
9,0,0,0
12,0,0,0
"""),2),
(parses(""" 0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
6,0,0,0
9,0,0,0
12,0,0,0
"""),1),
(parses("""-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0"""), 4),
(parses("""1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2"""), 3),
(parses("""1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2"""), 8),
]


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=25)
    data = parses(puzzle.input_data)

    for sample, sol in samples:
        assert constellations(sample) == sol
    puzzle.answer_a = constellations(data)
