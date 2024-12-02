import itertools
import math

from parse import parse


def parses(input):
    instructions, _, *nodes = input.strip().split("\n")
    nodes = [parse("{} = ({}, {})", node).fixed for node in nodes]
    return instructions, nodes


def solve_a(data):
    instructions, nodes = data
    map_ = {src: (L, R) for src, L, R in nodes}
    node = "AAA"
    for i, side in enumerate(itertools.cycle(instructions)):
        node = map_[node][side == "R"]
        if node == "ZZZ":
            return i + 1


def solve_b(data):
    instructions, nodes = data
    map_ = {src: (L, R) for src, L, R in nodes}
    nodes = [node for node in map_ if node.endswith("A")]

    periods = []
    for node in nodes:
        for i, side in enumerate(itertools.cycle(instructions)):
            node = map_[node][side == "R"]
            if node.endswith("Z"):
                periods.append(i + 1)
                break
    return math.lcm(*periods)


sample = parses(
    """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
)

sample2 = parses(
    """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
)

sample3 = parses(
    """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=8)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 2
    assert solve_a(sample2) == 6
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample3) == 6
    puzzle.answer_b = solve_b(data)
