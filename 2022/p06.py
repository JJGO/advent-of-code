def solve(data, n):
    for i in range(n, len(data)):
        if len(set(data[i - n : i])) == n:
            return i


def solve_a(data):
    return solve(data, 4)


def solve_b(data):
    return solve(data, 14)


samples = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
]


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=6)
    data = puzzle.input_data
    for sample, sol_a, sol_b in samples:
        assert solve_a(sample) == sol_a
        assert solve_b(sample) == sol_b

    puzzle.answer_a = solve_a(data)
    puzzle.answer_b = solve_b(data)
