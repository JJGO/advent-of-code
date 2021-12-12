import itertools
from heapq import heappush, heappop, heapify
import numpy as np


def parses(data):
    data = np.array([list(line) for line in data.strip().split("\n")])
    goblins = {tuple(pos): 200 for pos in np.argwhere(data == "G").tolist()}
    elves = {tuple(pos): 200 for pos in np.argwhere(data == "E").tolist()}
    wall = data == "#"
    return goblins, elves, wall


def solve_a(data):
    goblins, elves, wall = parses(data)
    for r in itertools.count():
        killed = set()
        for unit in sorted([*goblins, *elves]):
            # X is first dimension so in the render is "vertical"
            is_goblin = unit in goblins
            if unit not in killed:
                enemies = elves if is_goblin else goblins
                allies = goblins if is_goblin else elves
                if len(enemies) == 0:
                    return r * sum(allies.values())
                x, y = unit
                enemies_in_range = sorted(
                    [
                        (enemies[x2, y2], i, x2, y2)
                        for i, (x2, y2) in enumerate(
                            [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
                        )
                        if (x2, y2) in enemies
                    ]
                )

                if len(enemies_in_range) == 0:
                    # move
                    visited = set()
                    tovisit = [
                        (1, x - 1, y, x - 1, y),
                        (1, x, y - 1, x, y - 1),
                        (1, x, y + 1, x, y + 1),
                        (1, x + 1, y, x + 1, y),
                    ]
                    # We don't need to find all potential in-range points, just
                    # the closest and first in reading order will suffice
                    # The heap tracks (distance, RO in-range targer, RO first-step)
                    heapify(tovisit)
                    while tovisit:
                        d, x2, y2, nx, ny = heappop(tovisit)
                        if wall[x2, y2] or (x2, y2) in allies:
                            continue
                        for x2, y2 in [
                            (x2 - 1, y2),
                            (x2, y2 - 1),
                            (x2, y2 + 1),
                            (x2 + 1, y2),
                        ]:
                            if (x2, y2) not in visited:
                                if (x2, y2) in enemies:
                                    # print('GE'[is_elf],(x,y), 'moves', (nx,ny))
                                    allies[nx, ny] = allies.pop((x, y))
                                    x, y = nx, ny
                                    tovisit = []
                                    break
                                visited.add((x2, y2))
                                heappush(tovisit, (d + 1, x2, y2, nx, ny))

                enemies_in_range = sorted(
                    [
                        (enemies[x2, y2], i, x2, y2)
                        for i, (x2, y2) in enumerate(
                            [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
                        )
                        if (x2, y2) in enemies
                    ]
                )

                if len(enemies_in_range) > 0:
                    h, _, x2, y2 = enemies_in_range[0]
                    # print('GE'[is_elf],(x,y), 'strikes', (x2,y2))

                    if h > 3:
                        enemies[(x2, y2)] -= 3
                    else:
                        enemies.pop((x2, y2))
                        killed.add((x2, y2))

        # print(f'After {r+1} rounds')
        # render(goblins, elves, wall)
        # print()


def simulate(data, extra_power):
    goblins, elves, wall = parses(data)
    for r in itertools.count():
        killed = set()
        for unit in sorted([*goblins, *elves]):
            is_goblin = unit in goblins
            if unit not in killed:
                enemies = elves if is_goblin else goblins
                allies = goblins if is_goblin else elves
                if len(enemies) == 0:
                    return r * sum(allies.values())
                x, y = unit
                enemies_in_range = sorted(
                    [
                        (enemies[x2, y2], i, x2, y2)
                        for i, (x2, y2) in enumerate(
                            [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
                        )
                        if (x2, y2) in enemies
                    ]
                )

                if len(enemies_in_range) == 0:
                    visited = set()
                    tovisit = [
                        (1, x - 1, y, x - 1, y),
                        (1, x, y - 1, x, y - 1),
                        (1, x, y + 1, x, y + 1),
                        (1, x + 1, y, x + 1, y),
                    ]
                    heapify(tovisit)
                    while tovisit:
                        d, x2, y2, nx, ny = heappop(tovisit)
                        if wall[x2, y2] or (x2, y2) in allies:
                            continue
                        for x2, y2 in [
                            (x2 - 1, y2),
                            (x2, y2 - 1),
                            (x2, y2 + 1),
                            (x2 + 1, y2),
                        ]:
                            if (x2, y2) not in visited:
                                if (x2, y2) in enemies:
                                    allies[nx, ny] = allies.pop((x, y))
                                    x, y = nx, ny
                                    tovisit = []
                                    break
                                visited.add((x2, y2))
                                heappush(tovisit, (d + 1, x2, y2, nx, ny))

                enemies_in_range = sorted(
                    [
                        (enemies[x2, y2], i, x2, y2)
                        for i, (x2, y2) in enumerate(
                            [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
                        )
                        if (x2, y2) in enemies
                    ]
                )

                if len(enemies_in_range) > 0:
                    h, _, x2, y2 = enemies_in_range[0]
                    power = 3 if is_goblin else 3 + extra_power

                    if h > power:
                        enemies[(x2, y2)] -= power
                    else:
                        if (x2, y2) in elves:
                            return None
                        enemies.pop((x2, y2))
                        killed.add((x2, y2))


def solve_b(data):
    left = 0
    right = 200
    if (res := simulate(data, 0)) is not None:
        # No extra power needed
        return res
    assert simulate(data, right) is not None
    while right - left > 1:
        mid = (left + right) // 2
        res = simulate(data, mid)
        if res is None:
            left = mid
        else:
            right = mid
    return simulate(data, right)


def render(goblins, elves, wall):
    N, M = wall.shape

    for i in range(N):
        line = ""
        units = []
        for j in range(M):
            c = "#" if wall[i, j] else "."
            if (i, j) in elves:
                c = "E"
                units.append(f"E({elves[(i,j)]})")
            elif (i, j) in goblins:
                c = "G"
                units.append(f"G({goblins[(i,j)]})")
            line += c
        line = line + "    " + ", ".join(units)
        print(line)


sample = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""

samples = [
    """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""",
    """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""",
    """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""",
    """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""",
    """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""",
]

tricky_sample = """################################
###############.##...###########
##############..#...G.#..#######
##############.............#####
###############....G....G......#
##########..........#..........#
##########................##..##
######...##..G...G.......####..#
####..G..#G...............####.#
#######......G....G.....G#####E#
#######.................E.######
########..G...............######
######....G...#####E...G....####
######..G..G.#######........####
###.........#########.......E.##
###..#..#...#########...E.....##
######......#########.......####
#####...G...#########.....######
#####G......#########.....######
#...#G..G....#######......######
###...##......#####.......######
####..##..G........E...E..######
#####.####.....######...########
###########..#...####...E.######
###############...####..#...####
###############...###...#.E.####
#####################.#E....####
#####################.#...######
###################...##.#######
##################..############
##################...###########
################################"""


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=15)
    data = puzzle.input_data

    assert solve_a(sample) == 27730

    solutions = [36334, 39514, 27755, 28944, 18740]
    for s, sol in zip(samples, solutions):
        assert solve_a(s) == sol

    assert solve_a(tricky_sample) == 229798

    puzzle.answer_a = solve_a(data)

    samples2 = [sample, *samples[1:]]
    solutions2 = [4988, 31284, 3478, 6474, 1140]

    for s, sol in zip(samples2, solutions2):
        assert solve_b(s) == sol

    puzzle.answer_b = solve_b(data)
