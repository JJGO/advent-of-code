import parse
from collections import defaultdict


def parses(text):
    initial = parse.search("Begin in state {}.", text).fixed[0]
    steps = parse.search("Perform a diagnostic checksum after {:d} steps.", text).fixed[
        0
    ]
    DIRS = {"right": 1, "left": -1}
    states = {}
    for block in text.split("\n\n")[1:]:
        lines = block.split("\n")
        s = lines[0][-2]

        v0 = int(lines[2].strip(".").split(" ")[-1])
        m0 = DIRS[lines[3].strip(".").split(" ")[-1]]
        to0 = lines[4].strip(".").split(" ")[-1]

        v1 = int(lines[6].strip(".").split(" ")[-1])
        m1 = DIRS[lines[7].strip(".").split(" ")[-1]]
        to1 = lines[8].strip(".").split(" ")[-1]

        states[s] = [(v0, m0, to0), (v1, m1, to1)]
    return initial, states, steps


def solve_a(data):
    initial, states, steps = data
    tape = defaultdict(int)
    pos = 0
    current = initial
    for _ in range(steps):
        val, move, current = states[current][tape[pos]]
        tape[pos] = val
        pos += move
    return sum(tape.values())


sample = parses(
    """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2017, day=25)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 3
    puzzle.answer_a = solve_a(data)
