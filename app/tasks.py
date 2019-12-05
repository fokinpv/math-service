import math
from functools import lru_cache
from numba import njit


@lru_cache(None)
def ackermann(m, n):
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))


def factorial(n):
    return math.factorial(n)


@lru_cache(None)
def fibonacci(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)


@njit
def ackermann_nonrec(n, m):
    size = 0
    # FIXME hard coded array
    value = [0] * 10**6

    while 1:
        if m == 0:
            n += 1
            size -= 1
            if (size + 1) == 0:
                break
            m = value[size]
            continue

        if n == 0:
            m -= 1
            n = 1
            continue
        index = size
        size += 1
        value[index] = m - 1
        n -= 1

    return n
