import re
import math


def parse_workflow(line):
    name, workflow = line.strip("}").split("{")
    *rules, otherwise = workflow.split(",")
    mapping = {}
    for rule in rules:
        cond, dst = rule.split(":")
        mapping[cond] = dst
    mapping["x>0"] = otherwise  # trivially true
    return name, mapping


def parse_part(line):
    return eval(f"dict({line[1:-1]})")


def parses(input):
    workflows, parts = input.strip().split("\n\n")
    workflows = dict((parse_workflow(line) for line in workflows.split("\n")))
    parts = [parse_part(line) for line in parts.split("\n")]
    return workflows, parts


def solve_a(data):
    workflows, parts = data
    total = 0
    for part in parts:
        w = "in"
        while w not in "AR":
            rules = workflows[w]
            for rule, dst in rules.items():
                if eval(rule, None, part):
                    w = dst
                    break
        if w == "A":
            total += sum(part.values())
    return total


def solve_b(data):
    workflows, _ = data
    stack = [("in", {c: (1, 4001) for c in "xmas"})]
    total = 0

    while stack:
        node, constraints = stack.pop()
        for rule, dst in workflows[node].items():
            dim, side, val = re.match("(\w)([<>])(\d+)", rule).groups()
            val = int(val)
            low, high = constraints[dim]
            valid = constraints.copy()
            invalid = constraints.copy()

            if side == "<":
                valid[dim] = (low, min(high, val))
                invalid[dim] = (max(low, val), high)
            elif side == ">":
                valid[dim] = (max(low, val + 1), high)
                invalid[dim] = (low, min(high, val + 1))

            if valid[dim][0] < valid[dim][1]:
                if dst == "A":
                    total += math.prod((high - low for low, high in valid.values()))
                elif dst != "R":
                    stack.append((dst, valid))

            constraints = invalid
            if constraints[dim][0] >= constraints[dim][1]:
                break

    return total


sample = parses(
    """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=19)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 19114
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 167409079868000
    puzzle.answer_b = solve_b(data)
