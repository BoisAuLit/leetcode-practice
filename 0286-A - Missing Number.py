from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        return len(nums) * (len(nums) + 1) // 2 - sum(nums)


"""
Runtime
- 113ms
- Beats 99.30%

Memory
17.64mb
- Beats 79.16%
"""
