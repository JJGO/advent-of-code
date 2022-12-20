import math
import re
import numpy as np


def parses(input):
    costs = []
    # ore=0, clay=1, obsidian=2, geode=3 (robot, resource)
    idxs = np.array([(0, 0), (1, 0), (2, 0), (2, 1), (3, 0), (3, 2)])
    for line in input.strip().split("\n"):
        nums = re.findall(r"\d+", line)[1:]
        cost = np.zeros((4, 4), dtype=np.int32)
        cost[tuple(idxs.T)] = np.array(nums)
        costs.append(cost)
    return costs


def max_geodes(blueprint, mins):
    def H(mins, resources, robots):
        return tuple([mins] + resources.tolist() + robots.tolist())

    GEODE = 3
    max_cost = blueprint.max(axis=0)
    max_cost[GEODE] = mins

    stack = [
        (
            mins,
            np.array([0, 0, 0, 0], dtype=np.int32),
            np.array([1, 0, 0, 0], dtype=np.int32),
        )
    ]

    best_geodes = 0
    visited = set([H(*stack[0])])

    while stack:
        remaining, resources, robots = stack.pop()
        best_geodes = max(best_geodes, resources[GEODE])
        if remaining == 0:
            continue

        # We should drop a branch that cannot generate more geodes that the best case so far
        upper_bound = (
            resources[GEODE]
            + robots[GEODE] * remaining
            + remaining * (remaining - 1) / 2
        )
        if upper_bound <= best_geodes:
            continue

        for robot, cost in enumerate(blueprint):
            new_robots = robots.copy()
            new_robots[robot] += 1
            # 1: We should not have more resource supplying robots than what we can spend in a turn
            # 2: We can't wait to make something we are not collecting resources for
            # 3: We should not build a robot we could have build the previous iteration
            if (
                (new_robots > max_cost).any()
                or not (robots >= (cost > 0)).all()
                or (resources - cost >= cost).all()
            ):
                continue

            missing = cost - resources
            # We have N turns to collect missing resources and 1 turn to make the robot
            wait = 1 + int(
                max(np.ceil(missing[missing > 0] / robots[missing > 0]), default=0)
            )

            new_resources = resources + robots * wait - cost

            new = (remaining - wait, new_resources, new_robots)
            if wait <= remaining and (h := H(*new)) not in visited:
                visited.add(h)
                stack.append(new)

        # no-op till the end
        best_geodes = max(best_geodes, (resources + robots * remaining)[GEODE])

    return best_geodes


def solve_a(data):
    qs = [max_geodes(x, 24) for x in data]
    return sum((i * q for i, q in enumerate(qs, start=1)))


def solve_b(data):
    return math.prod([max_geodes(x, 32) for x in data[:3]])


sample = parses(
    """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=19)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 33
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 3472

    puzzle.answer_b = solve_b(data)
