from collections import defaultdict
import parse


def parses(input):
    vals = []
    for line in input.strip().split("\n"):
        vs = parse.parse(
            "Step {} must be finished before step {} can begin.", line
        ).fixed
        vals.append((vs[0], vs[1]))
    return vals


# Topological Sort
def topsort(steps):
    graph = defaultdict(list)
    n_incoming = defaultdict(int)
    for before, after in steps:
        graph[before].append(after)
        n_incoming[after] += 1
        n_incoming[before]
    no_incoming = sorted([k for k, v in n_incoming.items() if v == 0])

    top_order = []
    while len(no_incoming) > 0:
        node = no_incoming.pop(0)
        top_order.append(node)
        for child in graph[node]:
            n_incoming[child] -= 1
            if n_incoming[child] == 0:
                no_incoming.append(child)
        no_incoming.sort()
    return "".join(top_order)


# from networkx import DiGraph, lexicographical_topological_sort as lt_sort
# "".join(lt_sort(DiGraph((data))))


def mintime(steps, maxworkers=5, baseT=60):
    graph = defaultdict(list)
    n_incoming = defaultdict(int)
    for before, after in steps:
        graph[before].append(after)
        n_incoming[after] += 1
        n_incoming[before]
    ready = sorted([k for k, v in n_incoming.items() if v == 0])
    times = {k: ord(k) - ord("A") + 1 + baseT for k in n_incoming}

    time = 0
    completed = 0
    workers = [(None, None) for _ in range(maxworkers)]

    while True:
        for i, (task, eta) in enumerate(workers):
            if task is not None and (eta == time):
                completed += 1
                for child in graph[task]:
                    n_incoming[child] -= 1
                    if n_incoming[child] == 0:
                        ready.append(child)
                        ready.sort()
                workers[i] = (None, None)

        for i, (task, eta) in enumerate(workers):
            if task is None and len(ready) > 0:
                task = ready.pop(0)
                eta = time + times[task]
                workers[i] = (task, eta)
        if completed == len(times):
            break
        time = min(eta for _, eta in workers if eta)

    return time


sample = parses(
    """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=7)
    data = parses(puzzle.input_data)
    assert topsort(sample) == "CABDFE"
    puzzle.answer_a = topsort(data)
    assert mintime(sample, 2, 0) == 15
    puzzle.answer_b = mintime(data)
