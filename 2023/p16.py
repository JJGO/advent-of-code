def parses(input):
    return [list(row) for row in input.strip().split("\n")]


REFLECTIONS = {
    "-": {
        1: [-1j, 1j],
        -1: [-1j, 1j],
        1j: [1j],
        -1j: [-1j],
    },
    "|": {
        1j: [-1, 1],
        -1j: [-1, 1],
        1: [1],
        -1: [-1],
    },
    "/": {
        1j: [-1],
        -1j: [1],
        1: [-1j],
        -1: [1j],
    },
    "\\": {
        1j: [1],
        -1j: [-1],
        1: [1j],
        -1: [-1j],
    },
}


def simulate_reflections(data, initial):
    N, M = len(data), len(data[0])
    mirrors = {}
    for i in range(N):
        for j in range(M):
            if data[i][j] != ".":
                mirrors[i + 1j * j] = data[i][j]
    visited = set()
    stack = [initial]  # pos, dir
    while stack:
        pos, vel = stack.pop()
        pos += vel
        if not (0 <= pos.real < N and 0 <= pos.imag < M):
            continue
        if pos not in mirrors:
            visited.add((pos, vel))
            stack.append((pos, vel))
        else:
            mirror = mirrors[pos]
            for new_vel in REFLECTIONS[mirror][vel]:
                if (pos, new_vel) not in visited:
                    visited.add((pos, new_vel))
                    stack.append((pos, new_vel))

    energized = len(set(pos for pos, _ in visited))
    return energized


def solve_a(data):
    return simulate_reflections(data, (-1j, 1j))


def solve_b(data):
    N, M = len(data), len(data[0])
    initials = (
        [(i - 1j, 1j) for i in range(N)]
        + [(i + M * 1j, -1j) for i in range(N)]
        + [(-1 + j * 1j, 1) for j in range(M)]
        + [(N + j * 1j, -1) for j in range(M)]
    )
    return max(simulate_reflections(data, initial) for initial in initials)


sample = parses(
    r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=16)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 46
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 51
    puzzle.answer_b = solve_b(data)
