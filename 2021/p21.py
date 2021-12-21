import itertools
import functools
from collections import Counter, defaultdict
import parse


def parses(text):
    return [i[0] for i in parse.findall("position: {:d}", text)]


def move(pos):
    return 1 + (pos - 1) % 10


def solve_a(data):
    pos1, pos2 = data
    i = 1
    sc1, sc2 = 0, 0
    for i in itertools.count(1, 6):
        pos1 = move(pos1 + i + i + 1 + i + 2)
        sc1 += pos1
        if sc1 >= 1000:
            return (i + 2) * sc2
        i += 3
        pos2 = move(pos2 + i + i + 1 + i + 2)
        sc2 += pos2
        if sc2 >= 1000:
            return (i + 2) * sc1


def solve_b(data):
    """Each player is represented as dict[(pos, score), #ways]]
    We update each player indenpendenly and compute products
    of wins/loses to account for all possible universes
    """
    pos1, pos2 = data
    mem1, mem2 = {(pos1, 0): 1}, {(pos2, 0): 1}
    total1, total2 = 0, 0
    # Collapse 27 combinations into the 7 distinct moves (3..9) with counts
    steps = Counter(map(sum, itertools.product((1, 2, 3), repeat=3)))

    def turn(mem):
        # Runs turn for a single player
        wins = 0
        new_mem = defaultdict(int)
        for (pos, score), ways in mem.items():
            positions = {move(pos + step): n * ways for step, n in steps.items()}
            for new_pos, new_ways in positions.items():
                new_score = score + new_pos
                if new_score >= 21:
                    wins += new_ways
                else:
                    new_mem[new_pos, new_score] += new_ways
        return new_mem, wins

    while len(mem1) != 0 and len(mem2) != 0:
        mem1, wins1 = turn(mem1)
        total1 += wins1 * sum(mem2.values())
        mem2, wins2 = turn(mem2)
        total2 += wins2 * sum(mem1.values())

    return max(total1, total2)


def recursive_solve_b(data):
    # alternative slower recursive solution that might be easier to grok

    @functools.lru_cache(maxsize=None)
    def count_wins(p1, p2, sc1, sc2):
        # Player 1 is at position p1 with score sc1 and Player 2 is at position p2 with sc2
        # It's player 1 turn. Return the number of universes in which each player wins
        wins1, wins2 = 0, 0
        for step in map(sum, itertools.product((1, 2, 3), repeat=3)):
            new_p1 = (p1 + step - 1) % 10 + 1
            new_sc1 = sc1 + new_p1
            if new_sc1 >= 21:
                wins1 += 1
            else:
                w2, w1 = count_wins(p2, new_p1, sc2, new_sc1)
                wins1 += w1
                wins2 += w2
        return wins1, wins2

    return max(count_wins(*data, 0, 0))


sample = parses(
    """Player 1 starting position: 4
Player 2 starting position: 8"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=21)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 739785
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 444356092776315
    assert recursive_solve_b(sample) == 444356092776315
    puzzle.answer_b = solve_b(data)
