from collections import defaultdict
import toolz


def parses(input):
    initial, rules = input.strip().split("\n\n")
    initial = initial.split(": ")[1]
    rules = dict(line.split(" => ") for line in rules.split("\n"))
    rules = toolz.keymap(tuple, rules)
    return initial, rules


def propagate(initial, rules, ngen=20):
    state = defaultdict(lambda: ".")
    state.update({i: v for i, v in enumerate(initial)})
    l, r = 0, len(initial)
    for g in range(ngen):
        newstate = defaultdict(lambda: ".")
        for i in range(l - 4, r + 4):
            window = tuple(state[j] for j in range(i - 2, i + 3))
            newstate[i] = rules.get(window, ".")
            if newstate[i] == "#":
                l, r = min(l, i), max(r, i)
        state = newstate
    return sum(i for i, v in state.items() if v == "#")


def fast_propagate(initial, rules, ngen):
    state = defaultdict(lambda: ".")
    state.update({i: v for i, v in enumerate(initial)})
    l, r = 0, len(initial)
    history = [-1 for _ in range(5)]

    for g in range(ngen):
        newstate = defaultdict(lambda: ".")
        for i in range(l - 4, r + 4):
            window = tuple(state[j] for j in range(i - 2, i + 3))
            newstate[i] = rules.get(window, ".")
            if newstate[i] == "#":
                l, r = min(l, i), max(r, i)
        state = newstate
        nplants = sum(1 for i, v in state.items() if v == "#")
        s = sum(i for i, v in state.items() if v == "#")
        history.pop(0)
        history.append(nplants)
        if all(h == history[0] for h in history):
            return s + (ngen - g - 1) * nplants


sample = parses(
    """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""
)


if __name__ == "__main__":

    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=12)
    data = parses(puzzle.input_data)

    assert propagate(*sample) == 325
    puzzle.answer_a = propagate(*data)

    assert propagate(*sample, 1000) == fast_propagate(*sample, 1000)
    fast_propagate(*data, 50_000_000_000)
