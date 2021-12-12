from collections import defaultdict


def parses(input):
    graph = defaultdict(list)
    for src, dst in [line.split("-") for line in input.strip().split("\n")]:
        if dst != "start" and src != "end":
            graph[src].append(dst)
        if src != "start" and dst != "end":
            graph[dst].append(src)
    return graph


# No need to worry about cycles since a uppercase-cycle would
# lead to infinite paths so it's not a valid input
def solve(graph, part="a"):
    valid_paths = 0
    path_stack = [("start", "start", part == "b")]

    while path_stack:
        node, path, wildcard = path_stack.pop()
        for child in graph[node]:
            can_visit = child.isupper() or child not in path
            if can_visit or wildcard:
                if child == "end":
                    valid_paths += 1
                else:
                    child_wildcard = wildcard and can_visit
                    new_path = path + "," + child
                    path_stack.append((child, new_path, child_wildcard))

    return valid_paths


samples = [
    """start-A
start-b
A-c
A-b
b-d
A-end
b-end""",
    """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""",
    """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""",
]
samples = [parses(s) for s in samples]
solutions_a = [10, 19, 226]
solutions_b = [36, 103, 3509]

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=12)
    data = parses(puzzle.input_data)

    for sample, sol in zip(samples, solutions_a):
        assert solve(sample, "a") == sol
    puzzle.answer_a = solve(data, "a")

    for sample, sol in zip(samples, solutions_b):
        assert solve(sample, "b") == sol
    puzzle.answer_b = solve(data, "b")
