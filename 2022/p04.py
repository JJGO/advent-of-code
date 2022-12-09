import parse


def parses(input):
    return [
        parse.parse("{:d}-{:d},{:d}-{:d}", line).fixed
        for line in input.strip().split("\n")
    ]


def solve_a(data):
    return sum(
        (
            # (s2,e2) is fully contained in (s1,e1) if s1<=s2 and e2<=e1
            (s1 <= s2 and e2 <= e1) or (s2 <= s1 and e1 <= e2)
            for s1, e1, s2, e2 in data
        )
    )
    # Alt solution:  (s1 <= s2 <= e2 <= e1) or (s2 <= s1 <= e1 <= e2)


def solve_b(data):
    return sum(
        (
            # (s2,e2) overlaps (s1,e1) if it is not completely to the left or completely to the right
            not (e1 < s2 or s1 > e2)
            for s1, e1, s2, e2 in data
        )
    )
    # Verbose solution, check all four overlaps
    # (s1 <= s2 <= e1) or (s1 <= e2 <= e1) or (s2 <= s1 <= e2) or (s2 <= e1 <= e2)


sample = parses(
    """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=4)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 2
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 4
    puzzle.answer_b = solve_b(data)
