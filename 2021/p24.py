def parses(text):
    program = [line.split() for line in text.strip().split("\n")]
    program = [
        (instr, tuple([r if r in "wxyz" else int(r) for r in args]))
        for instr, *args in program
    ]
    return program


# Problem is obfuscated so solution is quite ugly
# You are pretty much forced to decompile the code, notice there's
# a repeating pattern of 18 instructions with three variables that change
# Variable A is either 1 or 26. When 26 we want x to be 0 to prevent the
# multiplication, otherwise there will be more multiplications by 25 than
# divisions by 26 and answer won't reach zero
# We can use A = 26 -> x = 0 to prune our search space and do the DFS
# so that digits are prioritized correctly


# Solution by reverse engineering
def solve_reveng(program, part):
    steps = [program[18 * i : 18 * (i + 1)] for i in range(14)]
    vals = [tuple(step[i][1][1] for i in [4, 5, 15]) for step in steps]

    def run_step(z, w, i):
        # Note code is not 1:1 mapping but black box
        # equivalent
        A, B, C = vals[i]
        x = int((z % 26) != w - B)
        z //= A
        z *= 25 * x + 1
        z += (w + C) * x
        return z, x

    stack = [(0, 0, tuple())]

    while True:
        z, i, seq = stack.pop()
        for w in range(1, 10) if part == "a" else range(9, 0, -1):
            z2, x = run_step(z, w, i)

            if vals[i][0] == 26 and x != 0:
                continue
            seq2 = seq + (w,)
            if z2 == 0 and i == 13:
                return int("".join(map(str, seq2)))
            elif i < 13:
                stack.append((z2, i + 1, seq2))


# A very interesting alternative solution is to ignore the code altogether
# and have a theorem prover like Z3 to perform symbolic execution with
# the specified restrictions. While Z3 can technically optimize, we can
# also solve the problem one digit at a time going from 9 to 1 as long as
# it is satisfiable we will eventually determine all digits
# The .push and .pop allow us to reuse part of the solver state


# Solution by symbolic execution
def solve_symexec(program, part):
    from z3 import If, Solver, simplify, BitVec, BitVecVal
    import operator

    zero = BitVecVal(0, 64)
    one = BitVecVal(1, 64)

    ops = {
        "add": operator.add,
        "sub": operator.sub,
        "mul": operator.mul,
        "div": operator.truediv,
        "mod": operator.mod,
        "eql": lambda a, b: If(a == b, one, zero),
    }

    def has_solution(solver, program, inputs):
        solver.push()
        i = 0
        regs = {k: zero for k in "wxyz"}

        for j, (instr, args) in enumerate(program):
            if instr == "inp":
                regs[args[0]] = inputs[i]
                i += 1
            else:
                a, b = args
                A = regs[a]
                B = regs[b] if b in regs else b

                if instr == "div":
                    solver.add(B != 0)
                elif instr == "mod":
                    solver.add(A >= 0)
                    solver.add(B > 0)

                regs[a] = BitVec(f"R{j:03d}", 64)
                solver.add(regs[a] == simplify(ops[instr](A, B)))

        solver.add(regs["z"] == 0)

        sat = str(solver.check()) == "sat"
        if not sat:
            solver.pop()
        return sat

    inputs = [BitVec(f"inp{i:02d}", 64) for i in range(14)]
    solver = Solver()
    for inp in inputs:
        solver.add(1 <= inp)
        solver.add(inp <= 9)

    for i in range(14):
        for n in range(9, 0, -1) if part == "a" else range(1, 10):
            inputs[i] = n
            if has_solution(solver, program, inputs):
                break
        else:
            raise ValueError("Unsatisfiable, look for bugs")
    return int("".join(map(str, inputs)))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=24)
    data = parses(puzzle.input_data)

    puzzle.answer_a = solve_reveng(data, "a")
    puzzle.answer_b = solve_reveng(data, "b")

    puzzle.answer_a = solve_symexec(data, "a")
    puzzle.answer_b = solve_symexec(data, "b")
