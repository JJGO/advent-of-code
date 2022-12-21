import functools
import operator
import z3
from sympy.solvers import solve
from sympy import Symbol

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


def parses(input):
    values = {}
    for line in input.strip().split("\n"):
        k, v = line.split(":")
        v = v.split()
        values[k] = int(v[0]) if len(v) == 1 else tuple(v)
    return values


# Data looks like a tree but it could be a DAG, so that's why
# the lru_cache is there. Idea is to recursive eval the tree
def eval_expression(data):
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "=": operator.eq,
    }

    @functools.lru_cache(maxsize=None)
    def memoize(monkey):
        v = data[monkey]
        if not isinstance(v, tuple):
            return v
        a, op, b = v
        return ops[op](memoize(a), memoize(b))

    return memoize("root")


def solve_a(data):
    return int(eval_expression(data))


# First solution I came up with is to be cheeky and just outsource
# the equation solving to z3, which allows us to reuse the evaluation
# code from before and just ask z3 for the value of X
def solve_b_z3(data):
    x = z3.Real("x")
    data = data.copy()
    data["humn"] = x
    a, _, b = data["root"]
    data["root"] = a, "=", b

    solver = z3.Solver()
    solver.add(eval_expression(data))
    if solver.check():
        return solver.model()[x].as_long()


# Another approach in the symbolic math realm is to use Sympy routines instead
# We just need to be careful with using round instead of int do the machine
# imprecision
def solve_b_sympy(data):
    x = Symbol('x', real=True)
    data = data.copy()
    data['humn'] = x
    a, _, b = data['root']
    data['root'] = a, '-', b
    eq = eval_expression(data)
    return round(solve(eq, x)[0])


# And for completeness we can of course do it manually which is likely the puzzle's
# intended solution. To achieve this, we can first simplify all branches of the tree
# independent of humn and then work our way down using reciprocal ops to solve for
# the unknown variable. Quite satisfying to get it working actually
def solve_b_manual(data):
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }
    simplified = {}
    to_simplify = []

    @functools.lru_cache(maxsize=None)
    def can_simplify(monkey):
        if monkey == "humn":
            return False

        v = data[monkey]
        if isinstance(v, int):
            simplified[monkey] = v
            return True
        a, op, b = v
        sa, sb = can_simplify(a), can_simplify(b)
        if sa and sb:  # ops over scalars
            simplified[monkey] = ops[op](simplified[a], simplified[b])
            return True
        else:
            to_simplify.append(monkey)
            return False

    can_simplify("root")

    while to_simplify:
        monkey = to_simplify.pop()
        a, op, b = data[monkey]
        a_ops = {
            "+": operator.sub,
            "-": operator.add,
            "*": operator.truediv,
            "/": operator.mul,
        }
        b_ops = {
            "+": operator.sub,
            "-": lambda x, y: y - x,
            "*": operator.truediv,
            "/": operator.truediv,
        }
        if monkey == "root":
            if a in simplified:
                simplified[b] = simplified[a]
            else:
                simplified[a] = simplified[b]
        else:
            if a in simplified:
                simplified[b] = b_ops[op](simplified[monkey], simplified[a])
            else:
                simplified[a] = a_ops[op](simplified[monkey], simplified[b])
    return int(simplified["humn"])


sample = parses(
    """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=21)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 152
    puzzle.answer_a = solve_a(data)

    for solve_b in (solve_b_z3, solve_b_sympy, solve_b_manual):
        assert solve_b(sample) == 301
        puzzle.answer_b = solve_b(data)
