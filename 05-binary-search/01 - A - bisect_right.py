from typing import List

"""
Simplified bisect_left(a, x) assuming:
- a is already sorted
- entire list is searched
"""


def bisect_right(a: List[int], x: int) -> int:
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo
