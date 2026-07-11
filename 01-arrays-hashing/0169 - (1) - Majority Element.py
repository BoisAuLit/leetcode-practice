from typing import List
from statistics import mode

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        return mode(nums)
        

s = Solution()
nums = [2, 2, 1, 1, 1, 2, 2]
result = s.majorityElement(nums)
print(result)
