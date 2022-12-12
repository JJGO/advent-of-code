import parse, copy, math


def parses(input):
    blocks = input.strip().split("\n\n")
    monkeys = [
        parse.parse(
            """Monkey {:d}:
  Starting items: {}
  Operation: new = {}
  Test: divisible by {:d}
    If true: throw to monkey {:d}
    If false: throw to monkey {:d}""",
            block,
        ).fixed
        for block in blocks
    ]

    def parse_op(op):
        if op == "old * old":
            return lambda x: x * x
        elif op.startswith("old * "):
            return lambda x: x * int(op.split()[-1])
        elif op.startswith("old + "):
            return lambda x: x + int(op.split()[-1])

    return [
        (
            [int(i) for i in starting.split(", ")],
            (parse_op(op), div, (m_false, m_true)),
        )
        for n, starting, op, div, m_true, m_false in monkeys
    ]


def solve_a(data):
    state = copy.deepcopy(data)
    times = [0 for _ in state]
    for _ in range(20):
        for i, (holding, logic) in enumerate(state):
            op, div, targets = logic
            times[i] += len(holding)
            for worry in holding:
                worry = op(worry) // 3
                throw = targets[worry % div == 0]
                state[throw][0].append(worry)
            state[i] = [], logic
    *_, a, b = sorted(times)
    return a * b


def solve_b(data):
    state = copy.deepcopy(data)
    times = [0 for _ in state]
    # poor man's lcm, divs are prime anyway
    MOD = math.prod([div for _, (_, div, _) in state])
    for _ in range(10_000):
        for i, (holding, logic) in enumerate(state):
            op, div, targets = logic
            times[i] += len(holding)
            for worry in holding:
                worry = op(worry) % MOD
                throw = targets[worry % div == 0]
                state[throw][0].append(worry)
            state[i] = [], logic
    *_, a, b = sorted(times)
    return a * b


sample = parses(
    """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=11)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 10605
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 2713310158
    puzzle.answer_b = solve_b(data)
