def parses(input):
    return [list(line) for line in input.strip().split("\n")]


def locations(data):
    obstacles = set()
    valid = set()
    guard = -1
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            if v == "#":
                obstacles.add(i + 1j * j)
            if v == ".":
                valid.add(i + 1j * j)

            if v == "^":
                if guard != -1:
                    raise ValueError
                guard = i + 1j * j
                valid.add(guard)

    return obstacles, valid, guard


def simulate_path(obstacles, valid, guard):
    mov, rot90 = -1, -1j

    visited = set([guard])
    while True:
        nextg = guard + mov
        while nextg in obstacles:
            mov = mov * rot90
            nextg = guard + mov

        if nextg not in valid:
            break
        visited.add(nextg)

        guard = nextg

    return visited


def loops(obstacles, valid, guard):
    mov, rot90 = -1, -1j

    visited = set([(guard, mov)])
    while True:
        nextg = guard + mov
        while nextg in obstacles:
            mov = mov * rot90
            nextg = guard + mov

        if nextg not in valid:
            return False
        if (nextg, mov) in visited:
            return True
        visited.add((nextg, mov))

        guard = nextg


def solve_a(data):
    obstacles, valid, guard = locations(data)
    return len(simulate_path(obstacles, valid, guard))


def solve_b(data):
    obstacles, valid, guard = locations(data)
    visited = simulate_path(obstacles, valid, guard)
    return sum([loops(obstacles | {k}, valid, guard) for k in visited])


sample = parses(
    """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
)


sample_loop = parses(
    """....#.....
.........#
..........
..#.......
.......#..
..........
.#.#^.....
........#.
#.........
......#..."""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=6)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 41
    puzzle.answer_a = solve_a(data)
    assert loops(*locations(sample_loop))
    assert solve_b(sample) == 6
    puzzle.answer_b = solve_b(data)
