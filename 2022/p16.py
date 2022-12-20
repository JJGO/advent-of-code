import re
import itertools
import functools


def parses(input):
    pattern = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    data = [re.findall(pattern, line)[0] for line in input.strip().split("\n")]
    return [(v, int(r), t.split(", ")) for v, r, t in data]


# A key trick is to "compress" the graph by only considering
# valves with nonzero pressure and computing the distance
# matrix between them. All-to-all shortest distance is O(N^3)
# via the Floyd-Warshall algorithm
def floyd_warshall(graph):
    D = {
        (i, j): 1 if i in graph[j] else float("inf")
        for i, j in itertools.product(graph, repeat=2)
    }
    for k, i, j in itertools.product(graph, repeat=3):
        D[i, j] = min(D[i, j], D[i, k] + D[k, j])
    return D


def preprocess(data):
    rates = {}
    graph = {}
    for valve, rate, neighbors in data:
        rates[valve] = rate
        graph[valve] = neighbors
    distances = floyd_warshall(graph)
    functioning_valves = [v for v, r in rates.items() if r > 0]
    return functioning_valves, distances, rates


# Part 1 can be done either with DFS or with Dynamic Programming
# We include top-down recursive DP as it is quite clean to
# implement and it extends nicely to part2
#
# Another important aspect is to move time in chunks, i.e. instead
# of 1 by 1, we instead consider the strategy of moving directly and
# opening the valve
def solve_a(data):
    functioning_valves, distances, rates = preprocess(data)

    @functools.lru_cache(maxsize=None)
    def max_pressure(remaining, location, state):
        # Stop option
        options = [remaining * rates[location]]
        # Open valve
        for i, valve in enumerate(functioning_valves):
            travel = distances[location, valve] + 1
            if not bool((state >> i) & 0x1) and travel < remaining:
                new_state = state | (1 << i)
                pressure = max_pressure(remaining - travel, valve, new_state)
                options.append(remaining * rates[location] + pressure)
        return max(options)

    return max_pressure(30, "AA", 0)


# Part 2 can be done with DP without blowing up the state by overlapping
# the work and state space. We let player 1 do a full pass and whenever
# it decides to stop, instead we now run the elephant just of the
# remaining open valves
def solve_b(data):
    functioning_valves, distances, rates = preprocess(data)

    @functools.lru_cache(maxsize=None)
    def max_pressure(remaining, location, state, elephant=False):
        # Stop option
        if elephant:
            options = [remaining * rates[location]]
        else:
            elephant_pressure = max_pressure(26, "AA", state, elephant=True)
            options = [remaining * rates[location] + elephant_pressure]
        # Open valve
        for i, valve in enumerate(functioning_valves):
            travel = distances[location, valve] + 1
            if not bool((state >> i) & 0x1) and travel < remaining:
                new_state = state | (1 << i)
                pressure = max_pressure(
                    remaining - travel, valve, new_state, elephant=elephant
                )
                options.append(remaining * rates[location] + pressure)
        return max(options)

    return max_pressure(26, "AA", 0)


# Another extremely neat way of solving part 2 is to perform the DP from part 1
# but keeping track of the max pressure per final state. That way we can then
# intersect disjoint states efficiently. The DP keeps track of a dict(state:pressure)
# instead of a single value. Finally, we sort states by value to skip lots of
# low pressure combinations
def solve_b(data):
    functioning_valves, distances, rates = preprocess(data)

    @functools.lru_cache(maxsize=None)
    def max_pressure_state(remaining, location, state):
        # Stop option
        options = {state: remaining * rates[location]}
        # Open valve
        for i, valve in enumerate(functioning_valves):
            travel = distances[location, valve] + 1
            if not bool((state >> i) & 0x1) and travel < remaining:
                new_state = state | (1 << i)
                for final, pressure in max_pressure_state(
                    remaining - travel, valve, new_state
                ).items():
                    options[final] = max(
                        options.get(final, 0), remaining * rates[location] + pressure
                    )
        return options

    # get the best split by final state
    per_state = max_pressure_state(26, "AA", 0)
    per_state = dict(sorted(per_state.items(), key=lambda x: -x[1]))
    # consider all disjoint combinations
    best = 0
    for mine, p1 in per_state.items():
        for elephant, p2 in per_state.items():
            if p1 + p2 < best:
                break
            if mine & elephant == 0:  # disjoint
                best = max(best, per_state[mine] + per_state[elephant])
    return best


sample = parses(
    """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=16)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 1651
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 1707
    puzzle.answer_b = solve_b(data)
