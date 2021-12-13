from p16 import ops
from sympy import divisors


def parses(data):
    ip_reg, *program = data.strip().split("\n")
    ip_reg = int(ip_reg[-1])
    program = [line.split(" ") for line in program]
    program = [(op, [int(i) for i in args]) for op, *args in program]
    return ip_reg, program


def solve_a(data):
    ip_reg, program = data
    ip = 0
    N = len(program)
    reg = [0] * 6
    while ip < N:
        opcode, args = program[ip]
        reg[ip_reg] = ip
        ops[opcode](reg, *args)
        ip = reg[ip_reg] + 1
    return reg[0]


def solve_b(data, reg0=1):
    """
    Tricky problem, it can be solved rather analitically
    I'm unsure how the input changes but the rough idea is as follows:

    After disassembling the code it can be simplified down to
    r4 = 989 if r0 == 0 else 10551389
    for r5 in range(r4):
        for r2 in range(r4):
            if i*j == r4:
                r0 += r5

    which for large numbers is still unwieldy to simulate.
    However we can easily solve it by realizing that we are just
    computing the sum of factors/divisors of r4
    """

    # Simulate until IP equals 3 so we know the loop amount
    ip_reg, program = data
    ip = 0
    reg = [reg0] + [0] * 5
    while ip != 3:
        opcode, args = program[ip]
        reg[ip_reg] = ip
        ops[opcode](reg, *args)
        ip = reg[ip_reg] + 1
    # Determine which register is used for the loop limit
    loop_reg = program[13][1][1]
    N = reg[loop_reg]
    # Compute sum of divisors
    return sum(divisors(N))


sample = parses(
    """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=19)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 6
    puzzle.answer_a = solve_a(data)
    assert solve_a(data) == solve_b(data, 0)
    puzzle.answer_b = solve_b(data)
