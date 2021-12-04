import parse


def parses(input):
    return [parse.parse("{} {:d}", line).fixed for line in input.strip().split("\n")]


def partA(cmds):
    h, v = 0, 0
    for cmd, x in cmds:
        if cmd == "up":
            v -= x
        elif cmd == "down":
            v += x
        elif cmd == "forward":
            h += x
    return h * v


def partB(cmds):
    h, v, a = 0, 0, 0
    for cmd, x in cmds:
        if cmd == "up":
            a -= x
        elif cmd == "down":
            a += x
        elif cmd == "forward":
            h += x
            v += a * x
    return h * v


sample = parses(
    """forward 5
down 5
forward 8
up 3
down 8
forward 2"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=2)
    data = parses(puzzle.input_data)
    assert partA(sample) == 150
    puzzle.answer_a = partA(data)
    assert partB(sample) == 900
    puzzle.answer_b = partB(data)
