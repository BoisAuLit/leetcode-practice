from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def canMakeArithmeticProgression(self, arr: List[int]) -> bool:
        min_value = min(arr)
        max_value = max(arr)
        diff = (max_value - min_value) / (len(arr) - 1)
        if diff == 0:
            return True
        if not diff.is_integer():
            return False
        set_ = set()
        for number in arr:
            if (number - min_value) % diff != 0:
                return False
            set_.add(number)
        return len(set_) == len(arr)


"""
Runtime
- 53ms
- Beats 76.10%

Memory
- 16.30mb
- Beats 98.20%
"""
