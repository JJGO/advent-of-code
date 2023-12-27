import itertools

EMPTY, WALL, ROCK = 0, 1, 2


def parses(input):
    return [[".#O".index(val) for val in line] for line in input.strip().split("\n")]


def as_coords(data):
    N = len(data)
    coords = [[] for _ in range(N)]
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if val in (ROCK, WALL):
                coords[N - 1 - j].append((i, val))
    return coords


def tilt(coords):
    new_coords = []
    for row in coords:
        last = -1
        new_coords.append([])
        for k, val in row:
            if val == WALL:
                last = k
            if val == ROCK:
                last += 1
            new_coords[-1].append((last, val))
    return new_coords


def load(coords):
    total_load = 0
    N = len(coords)
    for i, row in enumerate(coords):
        for j, val in row:
            if val == ROCK:
                total_load += N - j
    return total_load


def solve_a(data):
    return load(tilt(as_coords(data)))


def rotate(coords):
    N = len(coords)
    # i,j -> j, N-1-i
    new_coords = [[] for _ in range(N)]
    for i, row in enumerate(tilt(coords)):
        for j, val in row:
            new_coords[j].append((N - 1 - i, val))
    for j in range(N):
        new_coords[j] = sorted(new_coords[j])
    return new_coords


def coords_repr(coords):
    return tuple(
        [(i, j) for i, row in enumerate(coords) for j, val in row if val == ROCK]
    )


def solve_b(data):
    coords = as_coords(data)
    seen = {}
    loads = [load(coords)]
    for i in itertools.count(1):
        for _ in range(4):
            coords = rotate(tilt(coords))
        state = coords_repr(coords)
        loads.append(load(coords))
        if state not in seen:
            seen[state] = i
        else:
            j = seen[state]
            period = i - j
            offset = j - 1
            k = (1000000000 - offset) % period + offset
            return loads[k]


sample = parses(
    """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=14)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 136
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 64
    puzzle.answer_b = solve_b(data)
