from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        i = len(nums) - 2
        while i >= 0 and nums[i + 1] <= nums[i]:
            i -= 1
        if i == -1:
            nums.sort()
        j = len(nums) - 1
        while j >= 0 and nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
        nums[i + 1 :] = sorted(nums[i + 1 :])


s = Solution()

# Expecting [1,5,8,5,1,3,4,6,7]
input_ = [1, 5, 8, 4, 7, 6, 5, 3, 1]
result = s.nextPermutation(input_)

print(input_)

"""

"""
