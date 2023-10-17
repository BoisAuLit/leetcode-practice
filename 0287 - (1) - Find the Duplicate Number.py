from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        for num in nums:
            if nums[abs(num) - 1] < 0:
                return abs(num)
            nums[abs(num) - 1] *= -1


s = Solution()

# Expectin 2
input_ = [1, 3, 4, 2, 2]

result = s.findDuplicate(input_)
print(result)

"""

"""
