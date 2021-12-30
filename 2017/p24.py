import parse
from collections import defaultdict


def parses(text):
    return [parse.parse("{:d}/{:d}", line).fixed for line in text.strip().split("\n")]


def solve(data, part="a"):
    # Longest path in graph, NP-hard so we resort to brute force using DFS
    graph = defaultdict(list)

    for src, dst in data:
        graph[src].append(dst)
        graph[dst].append(src)

    stack = [(0, 0, 0, set())]
    max_ = 0 if part == "a" else (0, 0)

    while stack:
        val, length, src, visited = stack.pop()
        deadend = True
        for dst in graph[src]:
            edge = (min(src, dst), max(src, dst))
            if edge not in visited:
                new_visited = visited | set([edge])
                new_val = val + src + dst
                stack.append((new_val, length + 1, dst, new_visited))
                deadend = False
        if deadend:
            val = val if part == "a" else (length, val)
            max_ = max(max_, val)
    return max_ if part == "a" else max_[1]


sample = parses(
    """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2017, day=24)
    data = parses(puzzle.input_data)

    assert solve(sample, 'a') == 31
    puzzle.answer_a = solve(data, 'a')

    assert solve(sample, 'b') == 19
    puzzle.answer_b = solve(data, 'b')
