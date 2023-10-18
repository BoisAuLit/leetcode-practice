from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def arraySign(self, nums: List[int]) -> int:
        sign = 1
        for num in nums:
            if num == 0:
                return 0
            if num < 0:
                sign *= -1
        return sign


"""
Runtime
- 63ms
- Beats 92.77%

Memory
16.42mb
- Beats 64.48%
"""
