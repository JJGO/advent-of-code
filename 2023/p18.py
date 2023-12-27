from parse import parse


def parses(input):
    return [parse("{} {:d} (#{})", line).fixed for line in input.strip().split("\n")]


def solve_a(data):
    # shoelace manual
    x, y = 0, 0
    area, boundary = 0, 0
    moves = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
    for move, n, _ in data:
        dx, dy = moves[move]
        x2, y2 = x + n * dx, y + n * dy
        area += 1 / 2 * (x * y2 - x2 * y)
        x, y = x2, y2
        boundary += n
    return int(abs(area) + boundary / 2 + 1)


def solve_a_green(data):
    # green's theorem
    x = 0
    area, boundary = 0, 0
    moves = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
    for move, n, _ in data:
        dx, dy = moves[move]
        x += dx * n
        area += x * dy * n
        boundary += n
    return int(abs(area) + boundary / 2 + 1)


def solve_b(data):
    moves = {"0": "R", "1": "D", "2": "L", "3": "U"}
    data = [(moves[color[-1]], int(color[:-1], 16), None) for _, _, color in data]
    return solve_a(data)


sample = parses("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=18)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 62
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 952408144115
    puzzle.answer_b = solve_b(data)
