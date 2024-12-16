def parses(data):
    # Format is [size, id] where free space is id=None
    return [
        (size, k // 2 if k % 2 == 0 else None) for k, size in enumerate(map(int, data))
    ]


def range_sum(a, b):
    # Closed form of sum of range [a, b)
    return (a + (b - 1)) * ((b - 1) - a + 1) // 2


def solve_a(data):
    disk = data.copy()
    i, j = 0, len(disk) - 1

    # One pass, relocating intervals to free space
    compact_disk = []
    while i <= j:
        compact_disk.append(disk[i])
        free, _ = disk[i + 1]
        while free > 0:
            if i >= j:
                break
            size, fileid = disk[j]
            to_move = min(free, size)
            compact_disk.append((to_move, fileid))
            rem = size - to_move
            free -= to_move
            if rem > 0:
                disk[j] = (rem, fileid)
            else:
                j -= 2
        i += 2

    i, cksum = 0, 0
    for size, fileid in compact_disk:
        if fileid is not None:
            cksum += fileid * range_sum(i, i + size)
        i += size
    return cksum


def solve_b(data):
    files, holes = {}, []
    last = 0
    for size, fileid in data:
        if fileid is None:
            holes.append((last, size))
        else:
            files[fileid] = (last, size)
        last += size
    holes = holes[::-1] # reverse for more efficient popping

    fileid = max(files)
    # Attempt to move each file once, keep stack of leftmost free space
    while fileid > 0:
        loc, size = files[fileid]
        j = len(holes) - 1
        while j >= 0:
            freeloc, free = holes[j]
            if freeloc >= loc:
                break  # to the right
            if size <= free:
                files[fileid] = (freeloc, size)
                remainder = free - size
                if remainder > 0:
                    holes[j] = (freeloc + size, remainder)
                else:
                    holes.pop(j)
                break
            j -= 1
        fileid -= 1
    return sum(fileid * range_sum(i, i + size) for fileid, (i, size) in files.items())


sample = parses("""2333133121414131402""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=9)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 1928
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 2858
    puzzle.answer_b = solve_b(data)
