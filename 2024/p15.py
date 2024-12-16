from functools import cache


def parses(data):
    return data


def as_structs(data):
    board, moves = data.split("\n\n")
    board = [list(row) for row in board.split("\n")]
    moves = list(moves.replace("\n", ""))
    wall, boxes, robot = set(), set(), None
    for x, row in enumerate(board):
        for y, v in enumerate(row):
            pos = complex(x, y)
            if v == "#":
                wall.add(pos)
            if v == "O" or v == "[":
                boxes.add(pos)
            if v == "@":
                robot = pos
    dirs = {"<": -1j, ">": 1j, "v": 1, "^": -1}
    moves = [dirs[m] for m in moves]
    return wall, boxes, robot, moves


def gps(boxes):
    return sum((int(100 * pos.real + pos.imag) for pos in boxes))


def solve_a(data):
    wall, boxes, pos, moves = as_structs(data)
    for m in moves:
        if pos + m in wall:
            continue
        if pos + m not in boxes:
            pos += m
            continue
        box = pos + m
        while box in boxes:
            box += m
        if box in wall:
            continue
        boxes.remove(pos + m)
        boxes.add(box)
        pos = pos + m

    return gps(boxes)


def scale_up(board):
    board = board.replace("#", "##")
    board = board.replace("O", "[]")
    board = board.replace(".", "..")
    board = board.replace("@", "@.")
    return board


def solve_b(data):
    data = scale_up(data)
    wall, boxes, pos, moves = as_structs(data)

    for m in moves:
        newpos = pos + m
        if newpos in wall:
            # blocked by wall
            continue
        if newpos not in boxes and (newpos - 1j) not in boxes:
            # not blocked by box
            pos = newpos
            continue

        # blocked by box
        box = newpos if newpos in boxes else newpos - 1j

        would_move = set()

        @cache
        def move(box):
            would_move.add(box)
            needs_free = {
                1j: [box + m + 1j],
                -1j: [box + m],
                1: [box + m, box + m + 1j],
                -1: [box + m, box + m + 1j],
            }[m]

            for required in needs_free:
                if required in wall:
                    return False
                for other_box in (required, required - 1j):
                    if other_box in boxes and not move(other_box):
                        return False
            return True

        if not move(box):
            continue

        boxes = (boxes - would_move) | {b + m for b in would_move}
        pos = pos + m

    return gps(boxes)



sample = parses(
    """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=15)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 10092
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 9021
    puzzle.answer_b = solve_b(data)
