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


def sizes(root):
    all_sizes = []

    def _helper(node):
        size = 0
        for file, content in node.items():
            if isinstance(content, int):
                size += content
            elif isinstance(content, dict):
                size += _helper(content)
        all_sizes.append(size)
        return size

    _helper(root)
    return all_sizes


def solve_a(data):
    return sum(s for s in sizes(data) if s <= 100_000)


def solve_b(data):
    sizes_ = sizes(data)
    current_free = 70000000 - sizes_[-1]
    return min(s for s in sizes_ if (current_free + s) >= 30000000)


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
