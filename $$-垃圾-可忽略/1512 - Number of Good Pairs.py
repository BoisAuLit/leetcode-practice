from typing import List
from collections import Counter


class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        return sum(x * (x - 1) // 2 for x in Counter(nums).values())


# class Solution:
#     def numIdenticalPairs(self, nums: List[int]) -> int:
#         count = 0
#         for i in range(len(nums) - 1):
#             for j in range(i+1, len(nums)):
#                 if nums[i] == nums[j]:
#                     count += 1
#         return count


s = Solution()

# Expecting 4
input_ = [1, 2, 3, 1, 1, 3]

result = s.numIdenticalPairs(input_)
print(result)

"""

"""
