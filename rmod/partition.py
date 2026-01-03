from typing import Generator, List, Set


def enumerate_partitions(n: int) -> Generator[List[Set[int]], None, None]:
    if n == 0:
        yield []
        return
    if n == 1:
        yield [{0}]
        return

    for part in enumerate_partitions(n - 1):
        for i, cls in enumerate(part):
            new_part = [c.copy() for c in part]
            new_part[i].add(n - 1)
            yield new_part
        new_part = [c.copy() for c in part]
        new_part.append({n - 1})
        yield new_part


def bell_number(n: int) -> int:
    if n <= 1:
        return 1
    bell = [[0] * (n + 1) for _ in range(n + 1)]
    bell[0][0] = 1
    for i in range(1, n + 1):
        bell[i][0] = bell[i - 1][i - 1]
        for j in range(1, i + 1):
            bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1]
    return bell[n][0]
