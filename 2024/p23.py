"""The key idea when doing triangles and max-clique is to deduplicate
results by only growing subsets in a sorted order. For max-clique we also
prune the search space using the current best size (if the optimistic
clique is less than the best, drop that branch"""

from functools import reduce
import operator


def parses(data):
    return [tuple(line.split("-")) for line in data.strip().split("\n")]


def build_graph(data):
    graph = {}
    for a, b in data:
        graph[a] = graph.get(a, set()) | set([b])
        graph[b] = graph.get(b, set()) | set([a])
    return graph


def triangles(graph):
    triangles = []
    for node in sorted(graph):
        for neigh in graph[node]:
            if neigh < node:
                continue
            triangles += [
                (node, neigh, other)
                for other in graph[node] & graph[neigh]
                if neigh < other
            ]
    return triangles


def solve_a(data):
    tris = triangles(build_graph(data))
    return sum(1 for tri in tris if any(node.startswith("t") for node in tri))


def max_clique(graph):
    stack = [(n,) for n in sorted(graph)]

    max_clique = []

    while stack:
        nodes = stack.pop()
        if len(nodes) > len(max_clique):
            max_clique = nodes
        candidates = reduce(operator.and_, [graph[n] for n in nodes])
        candidates = [c for c in candidates if c > nodes[-1]]
        if len(nodes) + len(candidates) <= len(max_clique):
            continue  # prune when not going to improve
        for candidate in candidates:
            stack.append(nodes + (candidate,))
    return max_clique


def solve_b(data):
    return ",".join(max_clique(build_graph(data)))


### NetworkX solution

import itertools
import networkx as nx


def solve_a_nx(data):
    G = nx.Graph()
    G.add_edges_from(data)
    triangles = [
        nodes
        for nodes in itertools.takewhile(
            lambda x: len(x) <= 3, nx.enumerate_all_cliques(G)
        )
        if len(nodes) == 3 and any(n[0] == "t" for n in nodes)
    ]
    return len(triangles)

def solve_b_nx(data):
    G = nx.Graph()
    G.add_edges_from(data)
    return ",".join(sorted(max(nx.find_cliques(G), key=len)))


sample = parses(
    """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    for solve_a, solve_b in (solve_a, solve_b), (solve_a_nx, solve_b_nx):
        puzzle = Puzzle(year=2024, day=23)
        data = parses(puzzle.input_data)
        assert solve_a(sample) == 7
        puzzle.answer_a = solve_a(data)
        assert solve_b(sample) == "co,de,ka,ta"
        puzzle.answer_b = solve_b(data)
