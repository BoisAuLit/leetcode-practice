from typing import List

"""
Time complexity: O()
Space complexity: O()
"""

class Solution:
    def buildArray(self, nums: List[int]) -> List[int]:
        bit_length = (999).bit_length()
        mask = (1 << bit_length) - 1
        for i, v in enumerate(nums):
            nums[i] += (nums[v] & mask) << bit_length
        for i in range(len(nums)):
            nums[i] >>= bit_length
        return nums
            

s = Solution()
nums = [0,2,1,5,3,4] # Expecting [0,1,2,4,5,3]
result = s.buildArray(nums)
print(result)

"""
Runtime
- 127ms
- Beats 84.08%

Memory
- 16.67mb
- Beats 28.29%
"""
