import numpy as np

# Use a summed area table (dp)
def power(serial, part="a"):
    serial = int(serial)
    x = y = np.arange(300, dtype=np.int32)
    y, x = np.meshgrid(x, y)
    rack = x + 10
    power = rack * y + serial
    power = -5 + (power * rack // 100) % 10

    dp = np.zeros((301, 301), dtype=np.int32)
    for i in range(1, 301):
        for j in range(1, 301):
            dp[i, j] = (
                power[i - 1, j - 1] + dp[i - 1, j] + dp[i, j - 1] - dp[i - 1, j - 1]
            )

    def convolve(k):
        max_ = float("-inf")
        where = None
        for i in range(301 - k):
            for j in range(301 - k):
                val = dp[i + k, j + k] - dp[i + k, j] - dp[i, j + k] + dp[i, j]
                if val > max_:
                    max_ = val
                    where = (i, j)
        return (max_, *where)

    if part == "a":
        m, i, j = convolve(3)
        return f"{i},{j}"
    else:
        _, i, j, k = max(convolve(k) + (k,) for k in range(1, 301))
        return f"{i},{j},{k}"


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=11)
    data = int(puzzle.input_data)

    assert power(18, 'a') == '33,45'
    assert power(42, 'a') == '21,61'
    puzzle.answer_a = power(data, 'a')

    assert power(18, 'b') == '90,269,16'
    assert power(42, 'b') == '232,251,12'
    puzzle.answer_b = power(data, 'b')
