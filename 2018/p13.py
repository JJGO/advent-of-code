import numpy as np


def parses(input):
    return np.array([list(line) for line in input.split("\n")])


def first_collision(data):
    loc = data.copy()

    carts = newcarts = []
    occupied = set()
    for marker, vel in zip("<>^v", [(0, -1), (0, 1), (-1, 0), (1, 0)]):
        x, y = np.where(loc == marker)

        if len(x) > 0:
            for i, j in zip(x, y):
                carts.append((i, j, *vel, 0))
                occupied.add((i, j))

    while True:
        carts = sorted(newcarts)
        newcarts = []
        for x, y, vx, vy, n in carts:
            occupied.remove((x, y))
            x, y = x + vx, y + vy
            if (x, y) in occupied:
                return f"{y},{x}"
            if loc[x, y] == "\\":
                vx, vy = vy, vx
            elif loc[x, y] == "/":
                vx, vy = -vy, -vx
            elif loc[x, y] == "+":
                if n == 0:
                    a = 1 if vy == 0 else -1
                    vx, vy = a * vy, a * vx
                elif n == 2:
                    a = 1 if vx == 0 else -1
                    vx, vy = a * vy, a * vx
                n = (n + 1) % 3
            occupied.add((x, y))
            newcarts.append([x, y, vx, vy, n])


def all_collisions(data):
    loc = data.copy()

    carts = newcarts = []
    occupied = set()
    for marker, vel in zip("<>^v", [(0, -1), (0, 1), (-1, 0), (1, 0)]):
        x, y = np.where(loc == marker)

        if len(x) > 0:
            for i, j in zip(x, y):
                carts.append((i, j, *vel, 0))
                occupied.add((i, j))

    while True:
        carts = sorted(newcarts)
        newcarts = []
        for x, y, vx, vy, n in carts:
            if (x, y) in occupied:
                occupied.remove((x, y))
                x, y = x + vx, y + vy
                if (x, y) in occupied:
                    occupied.remove((x, y))
                    continue
                if loc[x, y] == "\\":
                    vx, vy = vy, vx
                elif loc[x, y] == "/":
                    vx, vy = -vy, -vx
                elif loc[x, y] == "+":
                    if n == 0:
                        a = 1 if vy == 0 else -1
                        vx, vy = a * vy, a * vx
                    elif n == 2:
                        a = 1 if vx == 0 else -1
                        vx, vy = a * vy, a * vx
                    n = (n + 1) % 3
                occupied.add((x, y))
                newcarts.append([x, y, vx, vy, n])
        if len(occupied) == 1:
            x, y = list(occupied)[0]
            return f"{y},{x}"
        newcarts = [c for c in newcarts if (c[0], c[1]) in occupied]


sampleA = parses(
    r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """
)

sampleB = parses(
    r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=13)
    data = parses(puzzle.input_data)

    assert first_collision(sampleA) == "7,3"
    puzzle.answer_a = first_collision(data)

    assert all_collisions(sampleB) == "6,4"
    puzzle.answer_b = all_collisions(data)
