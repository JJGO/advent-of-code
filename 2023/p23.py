from collections import defaultdict

import numpy as np

EMPTY, WALL, LEFT, RIGHT, UP, DOWN = range(6)


def parses(input):
    return [[".#<>^v".index(c) for c in line] for line in input.strip().split("\n")]


# LONGEST-PATH is NP-hard, so we have to brute-force it


def solve_a(data):
    data = np.array(data, dtype=np.uint8)

    map_ = {i + j * 1j: val for i, row in enumerate(data) for j, val in enumerate(row)}

    start = 1j * np.array([i for i, val in enumerate(data[0]) if val == EMPTY]).item()
    end = (
        len(data)
        - 1
        + 1j * np.array([i for i, val in enumerate(data[-1]) if val == EMPTY]).item()
    )

    stack = [(start, set([start]))]
    max_len = 0
    while stack:
        pos, visited = stack.pop()

        valid_directions = {
            EMPTY: [1, -1, 1j, -1j],
            LEFT: [-1j],
            RIGHT: [1j],
            UP: [-1],
            DOWN: [1],
        }[map_[pos]]

        for delta in valid_directions:
            new_pos = pos + delta
            if new_pos not in map_ or map_[new_pos] == WALL or new_pos in visited:
                continue
            if new_pos == end:
                max_len = max(max_len, len(visited))
                continue
            stack.append((new_pos, visited | set([new_pos])))

    return max_len


def find_intersections(data):
    data = np.array(data, dtype=np.int8)
    not_wall = np.pad(data != WALL, [(1, 1), (1, 1)])
    # intersections are not wall and have at least 3 not-wall neighbors
    intersections = (
        sum(
            [
                not_wall[2:, 1:-1],
                not_wall[:-2, 1:-1],
                not_wall[1:-1, 2:],
                not_wall[1:-1, :-2],
            ]
        )
        >= 3
    ) * not_wall[1:-1, 1:-1]
    intersection_coords = set([i + 1j * j for i, j in np.argwhere(intersections)])

    start = 1j * np.array([i for i, val in enumerate(data[0]) if val == EMPTY]).item()
    end = (
        len(data)
        - 1
        + 1j * np.array([i for i, val in enumerate(data[-1]) if val == EMPTY]).item()
    )

    intersection_coords |= set([start, end])
    return start, end, intersection_coords


def build_contracted_graph(map_, intersection_coords):
    distances = {}
    for node in intersection_coords:
        stack = [(node, 0, 0)]
        while stack:
            pos, prev_delta, pathlen = stack.pop()

            for delta in [1, -1, 1j, -1j]:
                new_pos = pos + delta
                if new_pos not in map_ or map_[new_pos] == WALL:
                    continue
                if delta == -prev_delta:
                    continue
                if new_pos in intersection_coords:
                    distances[node, new_pos] = pathlen
                    continue
                stack.append((new_pos, delta, pathlen + 1))
    return distances


def brute_force_longest_path(start, end, distances):
    graph = defaultdict(list)
    for (a, b), dist in distances.items():
        graph[a].append((b, dist + 1))
    # Small optim, once we visit the intersection connecting to the end
    # we have to exit, so we can stop at this point instead of the exit
    last_intersection, exit_dist = graph[end][0]
    stack = [(start, set([start]), 0)]
    max_len = 0
    while stack:
        node, visited, pathlen = stack.pop()

        for neigh, dist in graph[node]:
            if neigh == last_intersection:
                max_len = max(max_len, pathlen + dist + exit_dist)
                continue
            if neigh in visited:
                continue
            stack.append((neigh, visited | set([neigh]), pathlen + dist))
    return max_len


def solve_b(data):
    map_ = {i + j * 1j: val for i, row in enumerate(data) for j, val in enumerate(row)}
    start, end, intersection_coords = find_intersections(data)
    intersection_distances = build_contracted_graph(map_, intersection_coords)
    return brute_force_longest_path(start, end, intersection_distances)


sample = parses(
    """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=23)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 94
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 154
    puzzle.answer_b = solve_b(data)
