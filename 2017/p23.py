from sympy import primerange


def parses(text):
    return [tuple(line.split()) for line in text.strip().split("\n")]


def solve_a(program):
    regs = {c: 0 for c in "abcdefgh"}
    regs["1"] = 1
    ip = 0
    muls = 0
    while 0 <= ip < len(program):
        instr, x, y = program[ip]
        y = regs[y] if y in regs else int(y)
        if instr == "set":
            regs[x] = y
        elif instr == "sub":
            regs[x] -= y
        elif instr == "mul":
            regs[x] *= y
            muls += 1
        elif instr == "jnz":
            if regs[x] != 0:
                ip += int(y)
                continue
        ip += 1
    return muls


def solve_b(program):
    """
    Decompiled code amounts to:
    c = B + 17 * 1000
    for b in range(B, c+1, 17):
      f = 1
      for d in range(2, b+1):
        for e in range(2, b+1):
          if d * e == b:
            f = 0
      if f == 0:
        h += 1
    return h

    So we are counting composite numbers
    in the range(B, C+1, 17) where
    B, C are the values of b and c at IP=7.
    We can leverage sympy.primerange for that
    """

    regs = {c: 0 for c in "abcdefgh"}
    regs["a"] = 1
    regs["1"] = 1
    ip = 0
    for ip in range(0, 8):
        instr, x, y = program[ip]
        y = regs[y] if y in regs else int(y)
        if instr == "set":
            regs[x] = y
        elif instr == "sub":
            regs[x] -= y
        elif instr == "mul":
            regs[x] *= y
        elif instr == "jnz":
            if regs[x] != 0:
                ip += int(y)
                continue
        ip += 1
    start, end = regs["b"], regs["c"]
    q = -int(program[30][-1])
    N = len(range(start, end + 1, q))
    n_primes = sum(1 for p in primerange(start, end + 1) if (p - start) % 17 == 0)
    return N - n_primes


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2017, day=23)
    data = parses(puzzle.input_data)

    puzzle.answer_a = solve_a(data)
    puzzle.answer_b = solve_b(data)
