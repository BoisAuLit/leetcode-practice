from typing import List

"""
Simplified bisect_left(a, x) assuming:
- a is already sorted
- entire list is searched
"""


def bisect_left(a: List[int], x: int) -> int:
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo
