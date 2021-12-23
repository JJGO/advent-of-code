from p16 import ops


def parses(data):
    ip_reg, *program = data.strip().split("\n")
    ip_reg = int(ip_reg[-1])
    program = [line.split(" ") for line in program]
    program = [(op, [int(i) for i in args]) for op, *args in program]
    return ip_reg, program


# This problem requires disassembling the provided program
# A short summary is (for my input)
# 00-05 No-ops
# 06-07 R4 |= 1 << 6, R3 = A
# 08-16 R3 = f(R4); if R4 <= 256 GOTO 28
# 17-27 Perform Division of R4/256, GOTO 8
# 28-30 Halt if R3=R0 else GOTO 6


def solve_a(data):
    # First part is easy, we can simulate simulate
    # and stop when reaching instrunction pointer = 28
    # returning the contents of the register we compare R0 to
    ip_reg, program = data
    ip = 0
    N = len(program)
    reg = [0] * 6
    while ip < N:
        opcode, args = program[ip]
        reg[ip_reg] = ip
        ops[opcode](reg, *args)
        if ip == 28:
            return reg[args[0]]
        ip = reg[ip_reg] + 1


def solve_b(data):
    # Solves Part 2 for a generic input ignoring the program and
    # specific registers and extracting the magic constant from
    # the program
    # The last value is the one before we see a repeat and the
    # process effectively cycles
    ip_reg, program = data

    A, B, C = program[7][1][0], 0xFFFFFF, 65899
    Rx, Ry, Rz = 0, 0, 0

    seen = set()
    last = None

    Rx = 0x10000
    Rz = A
    while True:
        while Rx >= 256:
            Ry = Rx & 0xFF
            Rz = (((Rz + Ry) & B) * C) & B
            Rx >>= 8  # /=256, this encapsulates the count loop L17-25

        Ry = Rx & 0xFF
        Rz = (((Rz + Ry) & B) * C) & B
        if Rz in seen:
            return last
        last = Rz
        seen.add(last)
        Rx = Rz | 0x10000
        Rz = A


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=21)
    data = parses(puzzle.input_data)

    puzzle.answer_a = solve_a(data)
    puzzle.answer_b = solve_b(data)
