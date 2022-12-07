def parses(input):
    commands = [grp for grp in input.strip().split("$ ")]

    hierarchy = {"/": {}}
    pwd = hierarchy

    stack = []
    for command in commands:
        if command == "":
            continue
        cmd, *output = command.strip().split("\n")
        if cmd == "cd ..":
            pwd = stack.pop()
        elif cmd.startswith("cd"):
            _, arg = cmd.split(" ")
            stack.append(pwd)
            pwd = pwd.setdefault(arg, {})
        elif cmd == "ls":
            for line in output:
                size, file = line.split(" ")
                if size == "dir":
                    pwd[file] = {}
                else:
                    pwd[file] = int(size)
        else:
            print(command)
            raise ValueError()
    return hierarchy


def solve_a(data):
    def small_dirs(root):
        total_size = 0
        small_size = 0
        for file, content in root.items():
            if isinstance(content, int):
                total_size += content
            elif isinstance(content, dict):
                sub_size, sub_small = small_dirs(content)
                total_size += sub_size
                small_size += sub_small
        small_size += total_size * (total_size < 100_000)
        return total_size, small_size

    return small_dirs(data)[1]


def solve_b(data):
    sizes = []

    def compute_size(root):
        total_size = 0
        for file, content in root.items():
            if isinstance(content, int):
                total_size += content
            elif isinstance(content, dict):
                total_size += compute_size(content)
        sizes.append(total_size)
        return total_size

    total_size = compute_size(data)
    current_free = 70000000 - total_size
    min_free = 30000000 - current_free
    return sorted(i for i in sizes if i >= min_free)[0]


sample = parses(
    """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=7)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 95437
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 24933642
    puzzle.answer_b = solve_b(data)
