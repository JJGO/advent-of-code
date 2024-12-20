def parses(data):
    data = [list(line) for line in data.strip().split("\n")]
    return {(i, j): val for i, row in enumerate(data) for j, val in enumerate(row)}


def find_region(start, board):
    stack = [start]
    visited = set([start])
    while stack:
        i, j = stack.pop()
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neigh = i + di, j + dj
            if neigh in board and board[neigh] == board[start]:
                if neigh not in visited:
                    visited.add(neigh)
                    stack.append(neigh)
    return visited


def find_sides(visited, board):
    sides = {}
    for i, j in visited:
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neigh = i + di, j + dj
            if (neigh not in board) or (neigh not in visited):
                sides.setdefault((i, j), [])
                sides[i, j].append((di, dj))
    if len(visited) > 1:
        sides = {k: v for k, v in sides.items() if len(v) < 4}
    return sides


def deduplicate_sides(sides):
    # We only count each side once by counting the "leftmost" coordinate of each edge.
    # Leftmost is relative to the orientation, so we code it as a rotation
    unique_sides = {}
    for i, j in sides:
        for di, dj in sides[i, j]:
            neigh = i - dj, j + di  # rot90
            if neigh in sides and (di, dj) in sides[neigh]:
                continue
            unique_sides.setdefault((i, j), [])
            unique_sides[i, j].append((di, dj))
    return unique_sides


# Alternatively, we can count the number of corners which equals number of sides
def count_corners(sides):
    corners = 0
    for i, j in sides:
        for di, dj in sides[i, j]:
            di2, dj2 = -dj, di
            # convex
            if (di2, dj2) in sides[i, j]:
                corners += 1
            # concave
            i2, j2 = i + di - di2, j + dj - dj2
            if (i2, j2) in sides and (di2, dj2) in sides[i2, j2]:
                corners += 1
    return corners


def cost(board, bulk):
    visited = set()
    cost = 0
    for pos in board:
        if pos not in visited:
            region = find_region(pos, board)
            area = len(region)
            sides = find_sides(region, board)
            if bulk:
                sides = deduplicate_sides(sides)
            perim = sum([len(edges) for edges in sides.values()])
            visited |= region
            cost += area * perim
    return cost


def solve_a(data):
    return cost(data, bulk=False)


def solve_b(data):
    return cost(data, bulk=True)


sample = parses(
    """AAAA
BBCD
BBCC
EEEC """
)

sample2 = parses(
    """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
)

sample3 = parses(
    """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
)

sample4 = parses(
    """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
)

sample5 = parses(
    """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=12)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 140
    assert solve_a(sample2) == 772
    assert solve_a(sample3) == 1930
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 80
    assert solve_b(sample2) == 436
    assert solve_b(sample3) == 1206
    assert solve_b(sample4) == 236
    assert solve_b(sample5) == 368
    puzzle.answer_b = solve_b(data)
