from typing import List

"""
Time complexity: O()
Space complexity: O()
"""

class Solution:
    def buildArray(self, nums: List[int]) -> List[int]:
        width = (999).bit_length()
        mask = (1 << width) - 1
        for i in range(len(nums)):
            nums[i] = nums[i] << width
        for i in range(len(nums)):
            nums[i] = nums[i] + (nums[nums[i] >> width] >> width)
        for i in range(len(nums)):
            nums[i] = nums[i] & mask
        return nums

s = Solution()
nums = [0,2,1,5,3,4] # Expecting [0,1,2,4,5,3]
result = s.buildArray(nums)
print(result)

"""
Runtime
- 143ms
- Beats 9.45%

Memory
- 16.65mb
- Beats 28.44%
"""
