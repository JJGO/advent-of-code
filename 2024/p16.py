from heapq import heappush, heappop

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=16)


def parses(data):
    return data.strip().split("\n")


def as_sparse(lines):
    walls = set()
    start = None
    end = None
    for i, row in enumerate(lines):
        for j, v in enumerate(row):
            z = (i, j)
            if v == "S":
                assert start is None
                start = z
            if v == "E":
                assert end is None
                end = z
            if v == "#":
                walls.add(z)
    return walls, start, end


def solve_a(data):
    # Dijkstra's algorithm
    walls, start, end = as_sparse(data)
    heap = [(0, start, (0, 1))]
    visited = {}

    while heap:
        cost, pos, dir = heappop(heap)
        if (pos, dir) in visited:
            continue

        if pos == end:
            return cost

        visited[pos, dir] = cost

        # Keep direction
        nextpos = (pos[0] + dir[0], pos[1] + dir[1])
        if nextpos not in walls and (nextpos, dir) not in visited:
            heappush(heap, (cost + 1, nextpos, dir))

        # Change direction
        dx, dy = dir
        for nextdir in [(dy, -dx), (-dy, dx)]:
            if (pos, nextdir) not in visited:
                heappush(heap, (cost + 1000, pos, nextdir))


def solve_b(data):
    walls, start, end = as_sparse(data)
    start_dir = (0, 1)
    heap = [(0, start, start_dir, None, None)]
    visited = {}
    preds = {}

    ends, end_cost = [], None

    # Dijkstra's algorithm but we keep track of all paths to the end
    # by storing for each state all the previous states that lead to it
    # with the same cost

    # Here the state is defined by the position and the direction

    while heap:
        cost, pos, dir, prevpos, prevdir = heappop(heap)

        if (pos, dir) not in visited:
            preds[pos, dir] = [(prevpos, prevdir)]
        elif visited[pos, dir] == cost:
            preds[pos, dir].append((prevpos, prevdir))

        if (pos, dir) in visited:
            continue

        visited[pos, dir] = cost

        if pos == end:
            if end_cost is None:
                end_cost = cost
            if cost == end_cost:
                ends.append((pos, dir))
            continue

        nextpos = (pos[0] + dir[0], pos[1] + dir[1])
        if nextpos not in walls and (nextpos, dir) not in visited:
            heappush(heap, (cost + 1, nextpos, dir, pos, dir))

        dx, dy = dir
        for nextdir in [(dy, -dx), (-dy, dx)]:
            if (pos, nextdir) not in visited:
                heappush(heap, (cost + 1000, pos, nextdir, pos, dir))

    preds[start, start_dir] = []

    # We do backwards DFS from the end to the start using the predecessors map
    stack = ends
    unique = set([(end, None)])
    while stack:
        node = stack.pop()
        for pred in preds[node]:
            if pred not in unique:
                unique.add(pred)
                stack.append(pred)
    # We count the number of unique positions, ignoring the direction
    unique_pos = set([n for n, _ in unique])
    return len(unique_pos)


def solve_b_eq(data):
    walls, start, end = as_sparse(data)
    heap_start = [(0, start, (0, 1))]
    heap_end = [(0, end, d) for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
    cost_start, cost_end = {}, {}

    # run twice, from start and from end
    for heap, cost_from, target in [
        (heap_start, cost_start, end),
        (heap_end, cost_end, start),
    ]:
        while heap:
            cost, pos, dir = heappop(heap)
            if (pos, dir) in cost_from:
                continue

            cost_from[pos, dir] = cost

            if pos == target:
                continue
            nextpos = (pos[0] + dir[0], pos[1] + dir[1])
            if nextpos not in walls and (nextpos, dir) not in cost_from:
                heappush(heap, (cost + 1, nextpos, dir))

            dx, dy = dir
            for nextdir in [(dy, -dx), (-dy, dx)]:
                if (pos, nextdir) not in cost_from:
                    heappush(heap, (cost + 1000, pos, nextdir))

    best_cost = min([cost_start[pos, d] for pos, d in cost_start if pos == end])

    # Node is part of a optimal path if the sum of the cost from start and end is equal to the best cost
    best_nodes = set()
    for node, (dx, dy) in cost_start:
        # we need to flip dir as we are going from end to start
        if (node, (-dx, -dy)) in cost_end:
            total_cost = cost_start[node, (dx, dy)] + cost_end[node, (-dx, -dy)]
            if best_cost == total_cost:
                best_nodes.add(node)
    return len(best_nodes)


# Networkx solutions

import networkx as nx


def build_graph(lines):

    G = nx.DiGraph()
    N, M = len(lines), len(lines[0])
    start, end = None, None

    for i, row in enumerate(lines):
        for j, val in enumerate(row):
            pos = (i, j)
            if val == "#":
                continue
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                i2, j2 = (i + dx, j + dy)
                if 0 <= i2 < N and 0 <= j2 < M and lines[i2][j2] != "#":
                    G.add_edge((pos, (dx, dy)), ((i2, j2), (dx, dy)), weight=1)

                for rotdx, rotdy in [(dy, -dx), (-dy, dx)]:
                    G.add_edge((pos, (dx, dy)), (pos, (rotdx, rotdy)), weight=1000)
            if val == "S":
                start = pos
            if val == "E":
                end = pos

    # end can be reached from any orientation
    for orientation in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        G.add_edge((end, orientation), end, weight=0)

    return G, start, end


def solve_a_nx(data):
    G, start, end = build_graph(data)
    return nx.shortest_path_length(
        G, source=(start, (0, 1)), target=end, weight="weight"
    )


def solve_b_nx(data):
    G, start, end = build_graph(data)
    nodes = set()
    for path in nx.all_shortest_paths(
        G, source=(start, (0, 1)), target=end, weight="weight"
    ):
        nodes.update([n for n, _ in path[:-1]])  # ignore dummy end
    return len(nodes)


sample = parses(
    """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
)

sample2 = parses(
    """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=16)
    data = parses(puzzle.input_data)
    for solve_a in [solve_a, solve_a_nx]:
        assert solve_a(sample) == 7036
        assert solve_a(sample2) == 11048
        puzzle.answer_a = solve_a(data)
    for solve_b in [solve_b, solve_b_eq, solve_b_nx]:
        assert solve_b(sample) == 45
        assert solve_b(sample2) == 64
        puzzle.answer_b = solve_b(data)
