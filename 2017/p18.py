from collections import defaultdict, deque


def parses(text):
    return [line.split() for line in text.strip().split("\n")]


def solve_a(program):
    regs = defaultdict(int)
    stack = []
    ip = 0
    while True:
        instr, *args = program[ip]
        ip += 1
        if instr == "snd":
            stack.append(regs[args[0]])
            continue
        elif instr == "rcv":
            if int(regs[args[0]]) != 0:
                return int(stack[-1])
            continue
        a, b = args
        b = regs[b] if b.isalpha() else int(b)
        if instr == "jgz":
            if regs[a]:
                ip += b - 1
            continue
        elif instr == "set":
            regs[a] = b
        elif instr == "add":
            regs[a] += b
        elif instr == "mul":
            regs[a] *= b
        elif instr == "mod":
            regs[a] %= b


def solve_b(program):
    vals = [0, 0]

    def run_replica(program, qin, qout, id_):
        regs = defaultdict(int)
        regs["p"] = id_
        ip = 0
        while True:
            instr, *args = program[ip]
            a = args[0]
            A = regs[a] if a.isalpha() else int(a)
            if len(args) > 1:
                b = args[1]
                B = regs[b] if b.isalpha() else int(b)
            ip += 1
            if instr == "snd":
                vals[id_] += 1
                qout.append(A)
                continue
            elif instr == "rcv":
                if len(qin) > 0:
                    regs[a] = qin.popleft()
                    continue
                else:
                    ip -= 1
                    yield
            if instr == "jgz":
                if A > 0:
                    ip += B - 1
                    continue
            elif instr == "set":
                regs[a] = B
            elif instr == "add":
                regs[a] += B
            elif instr == "mul":
                regs[a] *= B
            elif instr == "mod":
                regs[a] %= B

    q0, q1 = deque(), deque()
    r0 = run_replica(program, q0, q1, 0)
    r1 = run_replica(program, q1, q0, 1)

    while True:
        next(r0)
        next(r1)
        if len(q0) == 0 and len(q1) == 0:
            return vals[1]


sample_a = parses(
    """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""
)

sample_b = parses(
    """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2017, day=18)
    data = parses(puzzle.input_data)

    assert solve_a(sample_a) == 4
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample_b) == 3
    puzzle.answer_b = solve_b(data)
