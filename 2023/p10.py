import numpy as np


def parses(input):
    table = str.maketrans("|-JL7F.", "│─┘└┐┌ ")
    return [list(line.translate(table)) for line in input.strip().split("\n")]


def find_boundary(data):
    DIRECTIONS = {  # map of tile, to exit directions
        "│": [1, -1],
        "─": [1j, -1j],
        "┘": [-1j, -1],
        "└": [1j, -1],
        "┐": [-1j, 1],
        "┌": [1j, 1],
    }
    # first dim is vertical, second horizontal
    exits = {}
    for tile, (d1, d2) in DIRECTIONS.items():
        exits[tile, -d1] = d2
        exits[tile, -d2] = d1

    # build map
    map_ = {}
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if val != " ":
                map_[i + 1j * j] = val
            if val == "S":
                start = i + 1j * j

    for direction in [1, -1, 1j, -1j]:
        initial_dir = direction
        current = start
        boundary = {}
        while True:
            neighbor = current + direction

            if neighbor not in map_:
                break

            if map_[neighbor] == "S":
                exits_to_tile = {}
                for tile, (d1, d2) in DIRECTIONS.items():
                    exits_to_tile[d1, d2] = tile
                    exits_to_tile[d2, d1] = tile
                start_tile = exits_to_tile[initial_dir, -direction]

                boundary[neighbor] = start_tile

                return boundary

            if (map_[neighbor], direction) not in exits:
                break

            current = neighbor
            direction = exits[map_[neighbor], direction]
            boundary[current] = map_[current]


def solve_a(data):
    boundary = find_boundary(data)
    return len(boundary) // 2


def solve_b_floodfill(data):
    # Convert to high resolution, do flood fill
    HIRES = {  # map of tile, to exit directions
        "│": [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
        "─": [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
        "┘": [[0, 1, 0], [1, 1, 0], [0, 0, 0]],
        "└": [[0, 1, 0], [0, 1, 1], [0, 0, 0]],
        "┐": [[0, 0, 0], [1, 1, 0], [0, 1, 0]],
        "┌": [[0, 0, 0], [0, 1, 1], [0, 1, 0]],
        " ": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    }

    boundary = find_boundary(data)
    N, M = len(data), len(data[0])

    # build hi-res map
    rows = []
    for i in range(N):
        blocks = []
        for j in range(M):
            tile = boundary.get(i + 1j * j, " ")
            blocks.append(np.array(HIRES[tile]))
        rows.append(np.hstack(blocks))
    map_ = np.vstack(rows).astype(np.uint8)

    # flood fill from top left corner
    stack = [(0, 0)]

    while stack:
        x, y = stack.pop()

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x2, y2 = x + dx, y + dy
            if not (0 <= x2 < 3 * N and 0 <= y2 < 3 * M):
                continue
            if map_[x2, y2] == 0:
                map_[x2, y2] = 2
                stack.append((x2, y2))

    inside = 0
    for i in range(N):
        for j in range(M):
            I, J = 3 * i, 3 * j
            block = map_[I : I + 3, J : J + 3]
            if np.all(block == 0):
                inside += 1
    return inside


def solve_b_math(data):
    boundary = [(x.real, x.imag) for x in find_boundary(data)]

    # area via Shoelace formula - https://en.wikipedia.org/wiki/Shoelace_formula
    points = boundary + [boundary[0]]
    area = (
        1
        / 2
        * abs(sum(x1 * y2 - y1 * x2 for (x1, y1), (x2, y2) in zip(points, points[1:])))
    )

    # pick's thm - area = inside + boundary/2 - 1
    inside = area - len(boundary) / 2 + 1
    return int(inside)

def solve_b_flip(data):
    # Graphics approach, start with outside and flip every time we see a vertical boundary
    # we need to pick either the bottom or top corners to count things correctly
    total = 0
    N, M = len(data), len(data[0])
    boundary = {(int(z.real), int(z.imag)): val for z, val in find_boundary(data).items()}
    for i in range(N):
        inside = False
        for j in range(M):
            total += ((i,j) not in boundary) and inside
            inside ^= boundary.get((i,j), ' ') in ('│┘└')
    return total


sample = parses(
    """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
)

sample2 = parses(
    """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""
)

sample3 = parses(
    """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
)

sample4 = parses(
    """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
)

sample5 = parses(
    """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=10)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 4
    assert solve_a(sample2) == 8
    puzzle.answer_a = solve_a(data)

    for solve_b in (solve_b_floodfill, solve_b_math):
        assert solve_b(sample3) == 4
        assert solve_b(sample4) == 8
        assert solve_b(sample5) == 10
        puzzle.answer_b = solve_b(data)
