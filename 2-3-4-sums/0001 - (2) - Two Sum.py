from typing import List

"""
Given an array of integers nums and an integer target,
return indices [A, B] such that array[A] + array[B] = target.

- There is exactly one solution.
- One element cannot be used twice.
- We can return the indices in any order.

Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        mapping = {}
        for index, number in enumerate(nums):
            complement = target - number
            if complement in mapping:
                return [index, mapping[complement]]
            mapping[number] = index


s = Solution()
input_ = [3, 2, 4]
result = s.twoSum(input_, 6)
print(result)
