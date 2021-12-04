def parses(input):
    return [int(i) for i in input.strip().split()]


def buildnode(data):
    nchild = data.pop(0)
    nmeta = data.pop(0)
    children = [buildnode(data) for i in range(nchild)]
    meta = [data.pop(0) for i in range(nmeta)]
    return (children, meta)


def tree(data):
    data = data.copy()
    return buildnode(data)


def sum_meta(node):
    children, meta = node
    return sum(meta) + sum(sum_meta(c) for c in children)


def nodeval(node):
    children, meta = node
    if len(children) == 0:
        return sum(meta)
    return sum(nodeval(children[m - 1]) for m in meta if m <= len(children))


sample = parses("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2")

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=8)
    data = parses(puzzle.input_data)
    assert sum_meta(tree(sample)) == 138
    puzzle.answer_a = sum_meta(tree(data))
    assert nodeval(tree(sample)) == 66
    puzzle.answer_b = nodeval(tree(data))
