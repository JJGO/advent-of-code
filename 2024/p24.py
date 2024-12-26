import parse


def parses(data):

    signals, gates = data.strip().split("\n\n")
    signals = dict(
        [parse.parse("{}: {:d}", line).fixed for line in signals.split("\n")]
    )
    gates = [parse.parse("{} {} {} -> {}", line).fixed for line in gates.split("\n")]
    gates = {c: (op, a, b) for a, op, b, c in gates}
    return signals, gates


def solve_a(data):
    signals, gates = data
    signals, gates = signals.copy(), gates.copy()

    OPS = {
        "AND": lambda x, y: x & y,
        "OR": lambda x, y: x | y,
        "XOR": lambda x, y: x ^ y,
    }

    changed = True
    while changed:
        changed = False

        for c, (op, a, b) in list(gates.items()):
            if a in signals and b in signals:
                signals[c] = OPS[op](signals[a], signals[b])
                gates.pop(c)
                changed = True

    num = 0
    for k, v in signals.items():
        if k.startswith("z") and v == 1:
            i = int(k[1:])
            num |= 1 << i
    return num


def solve_b(data):
    _, gates = data
    wrong = []
    highest_z = sorted([g for g in gates if g[0] == "z"])[-1]
    for c, (op, a, b) in sorted(gates.items()):

        valid = True

        # If it's an output, the operation must be an XOR (except for the last)
        if c[0] == "z":
            valid &= op == ("XOR" if c != highest_z else "OR")

        # If the operation is an XOR there are two cases:
        # 1. Either it's an output (z)
        # 2. It must take in both x and y (in any order)
        if op == "XOR":
            valid &= (c[0] == "z") or (["x", "y"] == sorted([a[0], b[0]]))

        # AND gates are used for carry, and must be followed by an OR, except 
        # the first carry gate x00 & y00
        if op == "AND":
            valid  &= (
                ['x00', 'y00'] == sorted([a, b]) or
                all(op2 == "OR" for _, (op2, a2, b2) in gates.items() if c in [a2, b2])
            )

        # OR & XOR gates must be followed by either
        # 1. An XOR for the sum gates
        # 2. An AND gate for the carry gates
        if op in ("OR", "XOR"):
            valid &= all(
                op2 in ["AND", "XOR"]
                for _, (op2, a2, b2) in gates.items()
                if c in [a2, b2]
            )

        if not valid:
            wrong.append(c)

    return ",".join(sorted(wrong))


sample = parses(
    """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""
)


sample2 = parses(
    """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=24)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 4
    assert solve_a(sample2) == 2024
    puzzle.answer_a = solve_a(data)
    puzzle.answer_b = solve_b(data)
