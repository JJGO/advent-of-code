import parse


def parses(input):
    return [tuple(line.split()) for line in input.strip().split("\n")]


# 0:Rock, 1:Paper, 2:Scissors
def as_ints(data):
    return [(ord(x) - ord("A"), ord(y) - ord("X")) for x, y in data]


def solve_a(data):
    data = as_ints(data)
    # mine-other mod 3 -> 0:draw, 1:win, 2:lose
    return sum(((1 + mine) + [3, 6, 0][mine - other % 3] for other, mine in data))


def solve_b(data):
    data = as_ints(data)
    # outcome + 2 mod 3 == mine - other mod 3
    # mine = (2+outcome+other) mod 3
    return sum(
        (
            (1 + ((outcome + 2 + other) % 3)) + [0, 3, 6][outcome]
            for other, outcome in data
        )
    )


sample = parses("""A Y
B X
C Z""")

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=2)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 15
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 12 
    puzzle.answer_b = solve_b(data)
