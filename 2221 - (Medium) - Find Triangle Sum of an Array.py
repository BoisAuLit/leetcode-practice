from typing import List


class Solution:
    def triangularSum(self, nums: List[int]) -> int:
        iteration = 0
        length = len(nums)
        while iteration != len(nums) - 1:
            iteration += 1
            for i in range(0, length - iteration):
                nums[i] = (nums[i] + nums[i + 1]) % 10

        return nums[0]
s = Solution()
nums = [1,2,3,4,5]
result = s.triangularSum(nums)
print(result)
