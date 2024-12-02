import parse


def parses(input):
    stacks, moves = input.strip("\n").split("\n\n")
    moves = [
        parse.parse("move {:d} from {:d} to {:d}", line).fixed
        for line in moves.split("\n")
    ]

    stacks = [list(line[1::4]) for line in stacks.split("\n")[:-1]]
    stacks = [
        [stacks[-i][j] for i in range(1, len(stacks) + 1) if stacks[-i][j] != " "]
        for j in range(len(stacks[0]))
    ]
    return stacks, moves


def solve(data, direction):
    stacks, moves = data
    stacks = [s.copy() for s in stacks]
    for n, src, dst in moves:
        src, dst = src - 1, dst - 1
        stacks[src], tail = stacks[src][:-n], stacks[src][-n:][::direction]
        stacks[dst].extend(tail)
    return "".join([s[-1] for s in stacks])


def solve_a(data):
    return solve(data, direction=-1)


def solve_b(data):
    return solve(data, direction=1)


sample = parses(
    """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=5)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == "CMZ"
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == "MCD"
    puzzle.answer_b = solve_b(data)
