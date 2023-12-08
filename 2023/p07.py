from collections import Counter


def parses(input):
    return [line.split() for line in input.strip().split("\n")]


def solve_a(data):
    vals = []
    for cards, bid in data:
        for c, r in zip("AKQJT", "edcba"):
            cards = cards.replace(c, r)
        f1, f2, *_ = [val for _, val in Counter(cards).most_common()] + [0]
        val = (f1, f2, cards, bid)
        vals.append(val)

    vals = sorted(vals)
    return sum(i * int(bid) for i, (*_, bid) in enumerate(vals, start=1))


def solve_b(data):
    vals = []
    for cards, bid in data:
        for c, r in zip("AKQJT", "edc1a"):
            cards = cards.replace(c, r)
        counts = Counter(cards.replace("1", "")).most_common()
        f1, f2, *_ = [val for _, val in counts] + [0, 0]
        f1 += cards.count("1")  # always better to have more of a card
        val = (f1, f2, cards, bid)
        vals.append(val)

    vals = sorted(vals)
    return sum(i * int(bid) for i, (*_, bid) in enumerate(vals, start=1))


sample = parses("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=7)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 6440
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 5905
    puzzle.answer_b = solve_b(data)
