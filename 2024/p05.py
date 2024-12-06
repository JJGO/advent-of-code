from collections import defaultdict
from functools import cmp_to_key


def parses(input):
    pre, post = input.split("\n\n")
    rules = [[int(k) for k in line.split("|")] for line in pre.split("\n")]
    pages = [[int(k) for k in line.split(",")] for line in post.split("\n")]
    return rules, pages


def solve_a(data):
    rules, updates = data
    total = 0

    follow = defaultdict(list)
    for x, y in rules:
        follow[x].append(y)

    for update in updates:
        order = {p: i for i, p in enumerate(update)}
        if all(order[p] < order[q] for p in update for q in follow[p] if q in update):
            total += update[len(update) // 2]
    return total


def solve_b(data):
    rules, updates = data
    total = 0

    follow = defaultdict(list)
    for x, y in rules:
        follow[x].append(y)

    def cmp(p, q):
        if q in follow[p]:
            return -1
        if p in follow[q]:
            return 1
        return 0

    for update in updates:
        order = {p: i for i, p in enumerate(update)}
        if not all(
            order[p] < order[q] for p in update for q in follow[p] if q in update
        ):
            update = sorted(update, key=cmp_to_key(cmp))
            total += update[len(update) // 2]
    return total


def solve_b_2(data):
    rules, updates = data
    total = 0

    follow = defaultdict(list)
    for x, y in rules:
        follow[x].append(y)

    def bubble_sorted(update):
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                p, q = update[i], update[j]
                if p in follow[q]:
                    update[i], update[j] = update[j], update[i]
        return update

    for update in updates:
        order = {p: i for i, p in enumerate(update)}
        if not all(
            order[p] < order[q] for p in update for q in follow[p] if q in update
        ):
            update = bubble_sorted(update)
            total += update[len(update) // 2]
    return total


sample = parses(
    """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=5)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 143
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 123
    puzzle.answer_b = solve_b(data)
