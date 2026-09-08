from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        left_sum = 0
        right_sum = sum(nums[1:])
        for i in range(len(nums)):
            if left_sum == right_sum:
                return i
            if i == len(nums) - 1:
                break
            left_sum += nums[i]
            right_sum -= nums[i + 1]
        return -1


"""
Runtime
- 171ms
- Beats 36.46%

Memory
17.72mb
- Beats 7.81%
"""
