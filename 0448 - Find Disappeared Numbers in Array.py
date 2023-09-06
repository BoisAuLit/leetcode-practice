from typing import List

class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        for num in nums:
            index = abs(num) - 1
            if nums[index] > 0:
                nums[index] *= -1
        return [index + 1 for index, num in enumerate(nums) if num > 0]


s = Solution()
input_ = [4, 3, 2, 7, 8, 2, 3, 1]
result = s.findDisappearedNumbers(input_)
print(result)

"""

"""
