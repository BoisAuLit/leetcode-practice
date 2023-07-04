from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        slow = fast = 0
        while True:
            while fast < len(nums) and nums[fast] == 0:
                fast += 1
            if fast >= len(nums):
                break
            nums[slow] = nums[fast]
            slow += 1
            fast += 1
        while slow < len(nums):
            nums[slow] = 0
            slow += 1


s = Solution()
nums = [0, 1, 0]
# nums = [0, 0, 0]
s.moveZeroes(nums)
print(nums)

"""
Runtime
- 180 ms
- Beats 53.86%

Memory
- 17.8 MB
- Beats 99.52%
"""
