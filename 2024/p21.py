"""
In order to solve this problem, it is key we exploit the structure of the setup.

- A key realization is that clicking any input on the numpad, requires clicking A on ALL
   directional pads, as it requires clicking A on the first robot, whose controlled by the second robot, &c
-  This means that each digit can be solved indenpendently. E.g Solving clicking 029A, reduces to solving
   1. move from A to 0  = <A
   2. move from 0 to 2  = ^A
   3. move from 2 to 9  = >^^A
   4. move from 0 to A  = vvvA
- We can treat the numpad as a "seed" sequence and then expand it at every step. See the example above for 029A

- We can empirically find that when moving, there's a priority
   0. Same move, e.g. we'll always prefer <<^ to <^<, as repeating a move is simply A. In practice this means
      that we ignore any zigzaggy pattern and focus solely on L-shaped moves
   1. < moving right is the most expensive move. We want to avoid sequences of the
        form A<A, as that "trip" can have been better used to click on any other button
   2. v similarly, moving down requires two moves from A
   3. ^> are equally distant from A

- For part2 the trick is realizing that the order doesn't really matter as rule expansion is purely local.
  This is further simplified by the fact that when translating a move to have an extra layer
  of indirection we can safely assume that it starts with "A", since the previous character had to be inputed
  by finished with A.
  Thus the solution has a "lanternfish" flavor of just needing to have a counter of all possible transitions
  and building a new one based on rule expansion.
"""

from functools import cache
from collections import Counter


def parses(data):
    return data.strip().split("\n")


@cache
def moves():
    buttons = "^<v>A"

    # This matrix is not arbitrary, on similar operations (e.g. <v vs v<), we choose to prioritize
    # the < over the v (and the v over ^>).
    move_table = [
        ["", "v<", None, "v>", ">"],
        [">^", "", ">", None, ">>^"],
        [None, "<", "", ">", "^>"],
        ["<^", None, "<", "", "^"],
        ["<", "v<<", "<v", "v", ""],
    ]

    move = {}  # dict of (src,dst) -> Moves a robot would have to do
    for i, a in enumerate(buttons):
        for j, b in enumerate(buttons):
            if move_table[i][j] is not None:
                move[a, b] = move_table[i][j] + "A"
    return move


def numpad_seq(src, dst):
    numpad = ["789", "456", "123", "X0A"]
    nums = {v: (i, j) for i, row in enumerate(numpad) for j, v in enumerate(row)}
    y1, x1 = nums[src]
    y2, x2 = nums[dst]
    hmoves = "<>"[x2 > x1] * abs(x1 - x2)
    vmoves = "^v"[y2 > y1] * abs(y1 - y2)
    if src in "741" and dst in "0A":  # can't go forbidden space
        return hmoves + vmoves + "A"
    if src in "0A" and dst in "741":  # can't go forbidden space
        return vmoves + hmoves + "A"
    if hmoves.startswith("<"):
        return hmoves + vmoves + "A"
    if vmoves.startswith("v"):
        return vmoves + hmoves + "A"
    return hmoves + vmoves + "A"  # doesn't matter


def solve_code(code):
    total_len = 0
    for src, dst in zip("A" + code, code):
        seq = numpad_seq(src, dst)
        for _ in range(2):
            seq = "".join((moves()[a, b] for a, b in zip("A" + seq, seq)))
        total_len += len(seq)
    return total_len, int(code[:-1])


def solve_a(data):
    return sum((length * num for length, num in map(solve_code, data)))


### PART 2


def as_transitions(seq):
    counts = Counter()
    for a, b in zip("A" + seq, seq):
        counts[a, b] += 1
    return counts


@cache
def move_transitions():
    return {k: as_transitions(v) for k, v in moves().items()}


def remote(counts):
    new_counts = Counter()
    for (src, dst), n in counts.items():
        for (a, b), m in move_transitions()[src, dst].items():
            new_counts[a, b] += n * m
    return new_counts


def solve_code_counts(code, n=25):
    total_len = 0
    for src, dst in zip("A" + code, code):
        trs = as_transitions(numpad_seq(src, dst))
        for _ in range(n):
            trs = remote(trs)
        total_len += sum(trs.values())
    return total_len, int(code[:-1])


def solve_b(data):
    return sum((length * num for length, num in map(solve_code_counts, data)))


sample = parses(
    """029A
980A
179A
456A
379A"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=21)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 126384
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 154154076501218  # unofficial
    puzzle.answer_b = solve_b(data)
