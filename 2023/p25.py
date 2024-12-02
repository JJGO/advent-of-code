import itertools
import math
import random
from collections import defaultdict, Counter, deque

import networkx as nx
import numpy as np

### MIN-CUT problem which has deterministic algo in polynomial time


def parses(input):
    graph = defaultdict(list)
    for line in input.strip().split("\n"):
        node, *neighs = line.replace(":", "").split()
        for neigh in neighs:
            graph[node].append(neigh)
    return dict(graph)


def build_nx_graph(graph):
    G = nx.Graph()
    for node, neighs in graph.items():
        for neigh in neighs:
            G.add_edge(node, neigh)
    # or just
    # G.add_edges_from(( (node, neigh) for node, neighs in graph.items() for neigh in neighs))
    return G


def solve_stoer_wagner(data):
    G = build_nx_graph(data)
    cut, partitions = nx.stoer_wagner(G)
    assert cut == 3
    return math.prod(map(len, partitions))


def solve_min_cut(data):
    G = build_nx_graph(data)
    for src, dst in G.edges():
        G[src][dst]["capacity"] = 1
    for src, dst in itertools.combinations(G, 2):
        cut, partitions = nx.minimum_cut(G, src, dst)
        if cut == 3:
            return math.prod(map(len, partitions))


def solve_spring(data):
    # Fruchterman-Reingold to find longest edges after simulating positions
    G = build_nx_graph(data)
    pos = nx.spring_layout(G)
    edge_dist = {
        (src, dst): np.linalg.norm(pos[src] - pos[dst]) for src, dst in G.edges()
    }
    min_cut = sorted(edge_dist, key=edge_dist.__getitem__)[-3:]
    G.remove_edges_from(min_cut)
    return math.prod(map(len, nx.connected_components(G)))


def build_undir_graph(data):
    graph = defaultdict(list)
    for node, neighs in data.items():
        for neigh in neighs:
            graph[node].append(neigh)
            graph[neigh].append(node)
    return dict(graph)


# fails for sample, works for data
def solve_random_paths(data):
    graph = build_undir_graph(data)

    # find shortest path between N random pairs, with high prob,
    # the min-cut edges will be the three most common visited edges

    n_iter = 300
    nodes = list(data)
    counter = Counter()
    for _ in range(n_iter):
        src, dst = random.choice(nodes), random.choice(nodes)
        queue = deque([src])
        visited = set()
        while queue:
            node = queue.popleft()
            for neigh in graph[node]:
                if neigh in visited:
                    continue
                visited.add(neigh)
                queue.append(neigh)
                canon_edge = tuple(sorted([node, neigh]))
                counter[canon_edge] += 1

    # cut the graph
    cut = [edge for edge, _ in counter.most_common()[:3]]
    for src, dst in cut + [(dst, src) for src, dst in cut]:
        graph[src] = [node for node in graph[src] if node != dst]

    # connected components with the cut
    visited = set()
    components = []
    for node in graph:
        if node in visited:
            continue
        stack = [node]
        size = 1
        visited.add(node)
        while stack:
            node = stack.pop()
            for neigh in graph[node]:
                if neigh in visited:
                    continue
                visited.add(neigh)
                size += 1
                stack.append(neigh)
        components.append(size)
    return math.prod(components)


def solve_grow_frontier(data):
    graph = build_undir_graph(data)
    node = next(iter(graph))
    visited = set([node])

    counts = Counter()
    while True:
        for neigh in graph[node]:
            if neigh not in visited:
                counts[neigh] += 1
        if len(counts) == 3:
            # we are at the min cut
            break
        node = counts.most_common()[0][0]
        del counts[node]
        visited.add(node)

    n = len(visited)
    N = len(graph)
    return n * (N - n)


# TODO Karger's algo


sample = parses(
    """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=25)
    data = parses(puzzle.input_data)
    for solve_a in [
        solve_min_cut,
        solve_stoer_wagner,
        solve_random_paths,
        solve_grow_frontier,
        solve_spring,
    ]:
        if solve_a not in (solve_random_paths, solve_grow_frontier):
            assert solve_a(sample) == 54
        puzzle.answer_a = solve_a(data)
