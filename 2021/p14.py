from collections import Counter
import parse
import more_itertools as mi


def parses(input):
    template, rules = input.split("\n\n")
    rules = {(a, b): c for a, b, c in parse.findall("{:l}{:l} -> {:l}", rules)}
    return template, rules


def solve_a(data, steps=10):
    template, rules = data
    for _ in range(steps):
        new = [rules[a, b] for a, b in zip(template, template[1:])]
        template = list(mi.interleave_longest(template, new))
    most, *_, least = Counter(template).most_common()
    return most[1] - least[1]


def solve_b(data, steps=40):
    template, rules = data
    pair_counts = Counter(zip(template, template[1:]))
    elements = Counter(template)

    for _ in range(steps):
        new_pair_counts = Counter()
        for (a, b), v in pair_counts.items():
            c = rules[(a, b)]
            new_pair_counts[(a, c)] += v
            new_pair_counts[(c, b)] += v
            elements[c] += v
        pair_counts = new_pair_counts

    return max(elements.values()) - min(elements.values())


sample = parses(
    """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=14)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 1588
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 2188189693529
    assert solve_a(data, 10) == solve_b(data, 10)
    puzzle.answer_b = solve_b(data)
