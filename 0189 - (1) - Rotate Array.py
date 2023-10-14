from typing import List

"""
Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.
"""

class Solution:
    def reverseArray(self, array: List[int], a: int, b: int) -> None:
        while a < b:
            array[a], array[b] = array[b], array[a]
            a += 1
            b -= 1

    def rotate(self, nums: List[int], k: int) -> None:
        k %= len(nums)
        self.reverseArray(nums, 0, len(nums) - 1)
        self.reverseArray(nums, 0, k - 1)
        self.reverseArray(nums, k, len(nums) - 1)


s = Solution()
nums = [1, 2, 3, 4, 5, 6, 7]
result = s.rotate(nums, 3)
print(nums)

"""

"""
