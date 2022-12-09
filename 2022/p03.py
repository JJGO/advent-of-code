def parses(input):
    return input.strip().split('\n')

def points(char):
    return 1 + ord(char.lower()) - ord("a") + 26 * char.isupper()


def solve_a(data):
    data = [(line[: len(line) // 2], line[len(line) // 2 :]) for line in data]
    chars = [(set(a) & set(b)).pop() for a, b in data]
    return sum(points(c) for c in chars)


def solve_b(data):
    chars = [
        (set(a) & set(b) & set(c)).pop()
        for a, b, c in zip(data[::3], data[1::3], data[2::3])
    ]
    return sum(points(c) for c in chars)


sample = parses(
    """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=3)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 157
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 70
    puzzle.answer_b = solve_b(data)
