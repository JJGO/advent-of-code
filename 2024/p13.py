from parse import parse
from fractions import Fraction

pattern = """Button A: X+{:d}, Y+{:d}
Button B: X+{:d}, Y+{:d}
Prize: X={:d}, Y={:d}"""


def parses(data):
    return [parse(pattern, line).fixed for line in data.strip().split("\n\n")]


def presses(machine, delta=0):
    xa, ya, xb, yb, px, py = [Fraction(x) for x in machine]
    px, py = px + delta, py + delta

    # Solve the system of equations by reduction
    a = (px / xb - py / yb) / (xa / xb - ya / yb)
    b = (px / xa - py / ya) / (xb / xa - yb / ya)

    # Check if the solution is integral
    if a.denominator == 1 and b.denominator == 1:
        a, b = a.numerator, b.numerator
        if (xa * a + xb * b == px) and (ya * a + yb * b == py):
            return 3 * a + b
    return 0


def solve_a(data):
    return sum(presses(machine) for machine in data)


def solve_b(data):
    N = 10000000000000
    return sum(presses(machine, N) for machine in data)


sample = parses(
    """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=13)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 480
    puzzle.answer_a = solve_a(data)
    puzzle.answer_b = solve_b(data)
