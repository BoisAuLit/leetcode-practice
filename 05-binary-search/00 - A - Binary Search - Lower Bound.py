from typing import List

"""
This is actually problem 0704 on leetcode.

Goal:
- Search for lower bound of element in array
- If element not found, return -1
"""


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)

        while left < right:
            mid = (left + right) // 2

            if nums[mid] < target: # ⭐️
                left = mid + 1
            else:
                right = mid

        if left < len(nums) and nums[left] == target: # ⭐️
            return left # ⭐️
        else:
            return -1

# Test case 1: Expecting 1
input_ = [1, 2, 2, 2, 2, 3]
s = Solution()
result = s.search(input_, 2)
print(result)
