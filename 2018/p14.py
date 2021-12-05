def partA(prefixlen):
    prefixlen = int(prefixlen)
    sb = [3, 7]
    e1, e2 = 0, 1
    while len(sb) < prefixlen + 10:
        s = sb[e1] + sb[e2]
        sb.extend(divmod(s, 10) if s >= 10 else [s])
        e1 = (1 + e1 + sb[e1]) % len(sb)
        e2 = (1 + e2 + sb[e2]) % len(sb)
    return "".join(map(str, sb[prefixlen:prefixlen+10]))

def partB(pattern):
    pattern = [int(i) for i in pattern]
    sb = [3, 7]
    e1, e2 = 0, 1
    while True:
        s = sb[e1] + sb[e2]
        for recipe in (divmod(s,10) if s >= 10 else [s]):
            sb.append(recipe)
            if sb[-len(pattern):] == pattern:
                return len(sb)-len(pattern)
        e1 = (1+e1+sb[e1]) % len(sb)
        e2 = (1+e2+sb[e2]) % len(sb)

samplesA = [
    (9, '5158916779'),
    (5, '0124515891'),
    (18, '9251071085'),
    (2018, '5941429882'),
]

samplesB = [
    ('51589', 9),
    ('01245', 5),
    ('92510', 18),
    ('59414', 2018),
]

if __name__ == "__main__":
    from aocd.models import Puzzle
    puzzle = Puzzle(year=2018, day=14)
    data = puzzle.input_data

    for n, sol in samplesA:
        assert partA(n) == sol
    puzzle.answer_a = partA(data)

    for n, sol in samplesB:
        assert partB(n) == sol
    puzzle.answer_b = partB(data)
