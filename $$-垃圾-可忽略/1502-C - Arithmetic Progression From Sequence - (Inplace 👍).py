from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def canMakeArithmeticProgression(self, arr: List[int]) -> bool:
        min_value = min(arr)
        max_value = max(arr)

        if (max_value - min_value) % (len(arr) - 1) != 0:
            return False
        diff = (max_value - min_value) // (len(arr) - 1)
        if diff == 0:
            return True
        for i, n in enumerate(arr):
            if n == min_value + i * diff:
                continue
            if (n - min_value) % diff != 0:
                return False
            j = (n - min_value) // diff
            if n == arr[j]:
                return False
            arr[i], arr[j] = arr[j], arr[i]
        return True


"""
Runtime
- 55ms
- Beats 64.21%

Memory
- 16.54mb
- Beats 14.64%
"""
