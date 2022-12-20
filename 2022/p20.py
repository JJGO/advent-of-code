from collections import deque


def parses(input):
    return [int(i) for i in input.strip().split("\n")]


#### First solution: Doubly Linked List with Modulo computations
# The idea is to represent the cyclic array with a doubly linked list
# and move items around by relocating them in the list.
# A key optimization/simplification is to note how things wrap around
# in a cyclic list. In a list with N elements, operations are mod (N-1)
# +1 -> +1
# +9 -> +0   # stepping N-1 times leaves us at the same arrangement
# +10 -> +1
# -1 -> +8

# Careful asignments are needed to relocate items in a Doubly Linked List


def mix_linkedlist(data, rounds):
    class ListNode:
        def __init__(self, val, next=None, prev=None):
            self.val = val
            self.next = next
            self.prev = prev

    N = len(data)
    nodes = [ListNode(i) for i in data]
    for i, _ in enumerate(data):
        nodes[i].next = nodes[(i + 1) % N]
        nodes[i].prev = nodes[i - 1]

    for _ in range(rounds):
        for n in nodes:
            steps = n.val % (N - 1)
            if steps == 0:
                continue
            dst = n
            for _ in range(steps):
                dst = dst.next

            n.prev.next, n.next.prev = n.next, n.prev
            dst_next = dst.next
            dst.next, dst_next.prev = n, n
            n.prev, n.next = dst, dst_next

    for node in nodes:
        if node.val == 0:
            break
    total = 0
    for i in range(1, 3001):
        node = node.next
        if i % 1000 == 0:
            total += node.val
    return total


#### Second solution: Array of indices
# The problem has a tricky aspect which makes it hard to use lists and it is
# the fact that the input contains duplicate entries so it is very hard
# to keep track of the original order, which is why LL made things simpler
# via pointers

# A very elegant solution is not to modify the array of values but rather
# the array of indices. I.e. we store the (cyclic) permutation array that
# represents the reordering. This way we can shuffle items around without
# confusion


def mix_indices(data, rounds):
    N = len(data)
    indices = list(range(N))

    for _ in range(rounds):
        for i in range(N):
            current_pos = indices.index(i)
            indices.pop(current_pos)
            next_pos = (current_pos + data[i]) % (N - 1)
            indices.insert(next_pos, i)
    j = indices.index(data.index(0))
    return sum(data[indices[(j + 1000 * i) % N]] for i in range(1, 4))


# 3. Use a Doubly Ended Queue - collections.deque to avoid having to
# implement a performant doubly linked list
# The ambiguity problem is dealt with by using tuples of (num, original pos)
# rather than the raw number.
# The logic is quite simple as we leverage the deque API
def mix_queue(data, rounds):
    N = len(data)
    values = [(n, i) for i, n in enumerate(data)]
    queue = deque(values)
    for _ in range(rounds):
        for val in values:
            j = queue.index(val)
            queue.rotate(-j)
            n, i = queue.popleft()
            moves = n % (N - 1)
            queue.rotate(-moves)
            queue.append((n, i))
    for i, (n, _) in enumerate(queue):
        if n == 0:
            break
    return sum(queue[(i + 1000 * j) % N][0] for j in range(1, 4))


mix = mix_indices


def solve_a(data):
    return mix(data, 1)


def solve_b(data):
    data = [i * 811589153 for i in data]
    return mix(data, 10)


sample = parses("1\n2\n-3\n3\n-2\n0\n4")

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=20)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 3
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 1623178306

    puzzle.answer_b = solve_b(data)
