from typing import List

"""
Time complexity: O(nlogn)
Space complexity: O(n) or O(logn)
"""


class Solution:
    def canMakeArithmeticProgression(self, arr: List[int]) -> bool:
        arr = sorted(arr)
        diff = arr[1] - arr[0]
        for i in range(len(arr) -1):
            if arr[i+1] - arr[i] != diff:
                return False
        return True

"""
Runtime
- 59ms
- Beats 38.94%

Memory
- 16.49mb
- Beats 54.86%
"""
