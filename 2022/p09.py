def parses(input):
    data = [line.split(" ") for line in input.strip().split("\n")]
    return [(d, int(i)) for d, i in data]


def sign(x):
    return complex((x.real > 0) - (x.real < 0), (x.imag > 0) - (x.imag < 0))


def solve_a(data):
    moves = {"R": 1, "L": -1, "U": 1j, "D": -1j}
    visited = set()
    H, T = 0, 0
    for direction, times in data:
        for _ in range(times):
            H += moves[direction]
            if abs(H - T) >= 2:
                T += sign(H - T)
            visited.add(T)
    return len(visited)


def solve_b(data):
    moves = {"R": 1, "L": -1, "U": 1j, "D": -1j}
    visited = set()
    rope = [0 for _ in range(10)]
    for direction, times in data:
        for _ in range(times):
            rope[0] += moves[direction]
            for i in range(1, 10):
                if abs(rope[i - 1] - rope[i]) >= 2:
                    rope[i] += sign(rope[i - 1] - rope[i])
            visited.add(rope[-1])
    return len(visited)


sample = parses(
    """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
)

sample_b = parses(
    """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=9)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 13
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 1
    assert solve_b(sample_b) == 36
    puzzle.answer_b = solve_b(data)
