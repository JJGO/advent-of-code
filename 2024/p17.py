from parse import parse

template = """Register A: {:d}
Register B: {:d}
Register C: {:d}

Program: {}"""


def parses(data):
    a, b, c, program = parse(template, data).fixed
    program = [int(x) for x in program.split(",")]
    return (a, b, c), program


def run_computer(registers, program):
    a, b, c = registers
    ip = 0
    output = []

    def combo(op):
        if op <= 3:
            return op
        if op <= 6:
            return [a, b, c][op - 4]
        raise ValueError("Invalid combo operand 7")

    while ip < len(program) - 1:
        op, val = program[ip : ip + 2]

        if op == 0:  # adv
            a = a >> combo(val)
        elif op == 1:  # bxl
            b ^= val
        elif op == 2:  # bst
            b = combo(val) & 7
        elif op == 3:  # jnz
            ip = val if a else ip + 2
        elif op == 4:  # bxc
            b ^= c
        elif op == 5:  # out
            output.append(combo(val) & 7)
        elif op == 6:  # bdv
            b = a >> combo(val)
        elif op == 7:  # cdv
            c = a >> combo(val)
        if op != 3:  # no jump
            ip += 2

    return output


def solve_a(data):
    return ",".join(str(x) for x in run_computer(*data))


def solve_b(data):
    _, program = data

    def to_decimal(seq):
        return sum(d * (8**i) for i, d in enumerate(reversed(seq)))

    # Search for solution using backtracking
    stack = [[i] for i in range(8)]

    while stack:
        seq = stack.pop()
        a = to_decimal(seq)
        output = run_computer((a, 0, 0), program)

        if output == program:
            return a

        # If current output matches target suffix, extend sequence
        n = len(output)
        if output[-n:] == program[-n:]:
            # reversed is important so we dfs smaller numbers first
            for i in reversed(range(8)):
                stack.append(seq + [i])


sample = parses(
    """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
)

sample_b = parses("""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=17)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == "4,6,3,5,6,3,5,2,1,0"
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample_b) == 117440
    puzzle.answer_b = solve_b(data)
