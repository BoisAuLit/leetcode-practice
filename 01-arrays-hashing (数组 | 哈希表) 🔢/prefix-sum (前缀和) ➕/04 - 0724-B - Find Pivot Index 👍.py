from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        sum_ = sum(nums)
        left_sum = 0
        for i in range(len(nums)):
            if left_sum == sum_ - nums[i] - left_sum:
                return i
            left_sum += nums[i]
        return -1


"""
Runtime
- 162ms
- Beats 63.37%

Memory
17.70mb
- Beats 7.81%
"""
