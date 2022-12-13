import json
import functools


def parses(input):
    data = []
    for pair in input.strip().split("\n\n"):
        left, right = pair.split("\n")
        data.append((json.loads(left), json.loads(right)))
    return data


def compare(a, b):
    # -1: a < b ,  0: a == b , 1: a > b
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0
    if isinstance(a, int):
        a = [a]
    if isinstance(b, int):
        b = [b]
    for i, j in zip(a, b):
        if (x := compare(i, j)) != 0:
            return x
    return compare(len(a), len(b))


def solve_a(data):
    return sum(i for i, s in enumerate(data, start=1) if compare(*s) == -1)


def solve_b(data):
    data = [val for pair in data for val in pair] + [[[2]], [[6]]]
    sorted_ = sorted(data, key=functools.cmp_to_key(compare))
    # Another alternative is to create a custom class that
    # only defines __lt__ using compare(self, other) == -1
    a = sorted_.index([[2]]) + 1
    b = sorted_.index([[6]]) + 1
    return a * b


sample = parses("""[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""")

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=13)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 13
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 140
    puzzle.answer_b = solve_b(data)
