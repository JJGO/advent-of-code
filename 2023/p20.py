from collections import deque
import math
import itertools


def parses(input):
    def parse_line(line):
        mod, dsts = line.split(" -> ")
        dsts = dsts.split(", ")
        if mod[0] in "%&":
            kind = {"%": "flip", "&": "conj"}[mod[0]]
            mod = mod[1:]
        elif mod == "broadcaster":
            kind = "cast"
        return mod, (kind, dsts)

    return [parse_line(line) for line in input.strip().split("\n")]


def solve_a(data):
    mods = dict(data)

    flip_states = {mod: 0 for mod, (kind, _) in data if kind == "flip"}
    conj_memory = {mod: {} for mod, (kind, _) in data if kind == "conj"}
    for mod, (kind, connected) in data:
        for dst in connected:
            if dst in conj_memory:
                conj_memory[dst][mod] = 0

    pulses = [0, 0]

    for i in range(1000):
        queue = deque([("broadcaster", dst, 0) for dst in mods["broadcaster"][1]])
        pulses[0] += 1 + len(queue)  # button + broadcasts

        while queue:
            src, mod, pulse = queue.popleft()
            if mod not in mods:
                continue

            kind, connected = mods[mod]
            if kind == "flip":
                if pulse == 1:
                    continue
                flip_states[mod] ^= 1
                new_pulse = flip_states[mod]
            elif kind == "conj":
                mem = conj_memory[mod]
                mem[src] = pulse
                new_pulse = 1 ^ all(s == 1 for s in mem.values())

            for dst in connected:
                pulses[new_pulse] += 1
                queue.append((mod, dst, new_pulse))

    return math.prod(pulses)


# The puzzle input is structured with 4 separate binary counters that
# count up to prime numbers and then reset to zero, thus we just
# need to find the periods of the high pulses going into the conjunction
# gate before rx
# Visualizing the input with graphviz is inmensely helpful
def solve_b(data):
    mods = dict(data)

    flip_states = {mod: 0 for mod, (kind, _) in data if kind == "flip"}
    conj_memory = {mod: {} for mod, (kind, _) in data if kind == "conj"}
    for mod, (kind, connected) in data:
        for dst in connected:
            if dst in conj_memory:
                conj_memory[dst][mod] = 0

    # find the nodes
    mods = dict(data)
    reverse = {}
    for mod, (kind, connected) in data:
        for dst in connected:
            reverse[dst] = reverse.get(dst, []) + [mod]
    prev = reverse["rx"][0]

    periods = {}

    for i in itertools.count(1):
        queue = deque([("broadcaster", dst, 0) for dst in mods["broadcaster"][1]])

        while queue:
            src, mod, pulse = queue.popleft()

            if mod == prev and pulse == 1:
                periods[src] = i
                if len(periods) == 4:
                    return math.lcm(*periods.values())

            if mod not in mods:
                continue

            kind, connected = mods[mod]
            if kind == "flip":
                if pulse == 1:
                    continue
                flip_states[mod] ^= 1
                new_pulse = flip_states[mod]
            elif kind == "conj":
                mem = conj_memory[mod]
                mem[src] = pulse
                new_pulse = 1 ^ all(s == 1 for s in mem.values())

            for dst in connected:
                queue.append((mod, dst, new_pulse))


sample = parses(
    """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
)

sample2 = parses(
    """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=20)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 32000000
    assert solve_a(sample2) == 11687500
    puzzle.answer_a = solve_a(data)
    puzzle.answer_b = solve_b(data)
