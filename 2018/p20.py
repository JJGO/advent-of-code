from heapq import heappush, heappop
from collections import namedtuple, defaultdict

BasePoint = namedtuple("BasePoint", "x, y")


class Point(BasePoint):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


def build_graph(regex):
    regex = regex.strip("^$")
    graph = defaultdict(set)
    start_stack = []
    end_stack = []
    # non-deterministic postion list
    current_pos = set([Point(0, 0)])
    moves = {"N": Point(-1, 0), "S": Point(1, 0), "E": Point(0, 1), "W": Point(0, -1)}
    for c in regex:
        if m := moves.get(c, None):
            for p in current_pos:
                graph[p].add(p + m)
                graph[p + m].add(p)
            current_pos = set(p + m for p in current_pos)
        elif c == "(":
            start_stack.append(current_pos.copy())
            end_stack.append(set())
        elif c == "|":
            end_stack[-1] |= current_pos
            current_pos = start_stack[-1].copy()
        elif c == ")":
            start_stack.pop()
            end_stack[-1] |= current_pos
            current_pos = end_stack.pop()
    return graph

def dijkstra(graph):
    distances = {}
    heap = [(0, Point(0,0))]
    while heap:
        d, pos = heappop(heap)
        if pos in distances:
            continue
        distances[pos] = d
        for neighbor in graph[pos]:
            if neighbor not in distances:
                heappush(heap, (d+1, neighbor))
    return distances

def solve_a(data):
    distances = dijkstra(build_graph(data))
    return max(distances.values())

def solve_b(data):
    distances = dijkstra(build_graph(data))
    return sum(1 for v in distances.values() if v >= 1000)

samples_a = [
    ('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$', 23),
    ('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$', 31),
]


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=20)
    data = puzzle.input_data

    for sample, sol in samples_a:
        assert solve_a(sample) == sol

    puzzle.answer_a = solve_a(data)
    puzzle.answer_b = solve_b(data)
