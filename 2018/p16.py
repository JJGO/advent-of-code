import operator
import re
from functools import reduce


def parses(data):
    trace, program = data.strip().split("\n" * 4)
    trace = [
        [[int(i) for i in re.findall(r"-?\d+", line)] for line in t.split("\n")]
        for t in trace.split("\n\n")
    ]
    program = [[int(i) for i in line.split(" ")] for line in program.split("\n")]
    return trace, program


def build_opr(bin_op):
    def _op(reg, a, b, c):
        reg[c] = bin_op(reg[a], reg[b])

    return _op


def build_opi(bin_op):
    def _op(reg, a, b, c):
        reg[c] = bin_op(reg[a], b)

    return _op


def setr(reg, a, _, c):
    reg[c] = reg[a]


def seti(reg, a, _, c):
    reg[c] = a


def gtir(reg, a, b, c):
    reg[c] = int(a > reg[b])


def gtri(reg, a, b, c):
    reg[c] = int(reg[a] > b)


def gtrr(reg, a, b, c):
    reg[c] = int(reg[a] > reg[b])


def eqir(reg, a, b, c):
    reg[c] = int(a == reg[b])


def eqri(reg, a, b, c):
    reg[c] = int(reg[a] == b)


def eqrr(reg, a, b, c):
    reg[c] = int(reg[a] == reg[b])


ops = {
    "addr": build_opr(operator.add),
    "addi": build_opi(operator.add),
    "mulr": build_opr(operator.mul),
    "muli": build_opi(operator.mul),
    "borr": build_opr(operator.or_),
    "bori": build_opi(operator.or_),
    "banr": build_opr(operator.and_),
    "bani": build_opi(operator.and_),
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
}


def solve_a(data):
    trace, _ = data
    total = 0
    for before, (code, *args), after in trace:
        valid_ops = set()
        for op, op_fn in ops.items():
            reg = before.copy()
            op_fn(reg, *args)
            if reg == after:
                valid_ops.add(op)
        total += len(valid_ops) >= 3
    return total


def get_mapping(trace):
    mapping = {i: set(ops) for i in range(16)}
    for before, (code, *args), after in trace:
        valid_ops = set()
        for op, op_fn in ops.items():
            reg = before.copy()
            op_fn(reg, *args)
            if reg == after:
                valid_ops.add(op)
        mapping[code] &= valid_ops

    while any(len(v) > 1 for v in mapping.values()):
        solved = reduce(operator.or_, [v for v in mapping.values() if len(v) == 1])
        mapping.update({k: v - solved for k, v in mapping.items() if len(v) > 1})
    mapping = {k: list(v)[0] for k, v in mapping.items()}
    return mapping


def run_program(mapping, program):
    reg = [0, 0, 0, 0]
    for code, *args in program:
        ops[mapping[code]](reg, *args)
    return reg


def solve_b(data):
    trace, program = data
    mapping = get_mapping(trace)
    reg = run_program(mapping, program)
    return reg[0]


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=16)
    data = parses(puzzle.input_data)

    puzzle.answer_a = solve_a(data)
    puzzle.answer_b = solve_b(data)
