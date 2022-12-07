import parse

def parses(input):
    return [parse.parse('{:d}-{:d},{:d}-{:d}', line).fixed 
            for line in input.strip().split('\n')]

def solve_a(data):
    return sum((
        ((l1 >= l2) and (r1 <= r2)) or
        ((l2 >= l1) and (r2 <= r1))
        for l1, r1, l2, r2 in data
    ))

def solve_b(data):
    return sum((
        (l1 <= l2 <= r1) or (l1 <= r2 <= r1) or 
        (l2 <= l1 <= r2) or (l2 <= r1 <= r2)
        for l1, r1, l2, r2 in data
    ))

sample = parses("""2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=4)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 2
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 4
    puzzle.answer_b = solve_b(data)
