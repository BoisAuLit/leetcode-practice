from typing import List
from bisect import bisect_left, bisect_right


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        if n == 0:
            return [-1, -1]
        lower = bisect_left(nums, target)

        if not 0 <= lower <= n - 1 or nums[lower] != target:
            return [-1, -1]

        upper = bisect_right(nums, target)

        return [lower, upper - 1]


# class Solution:
#     def searchRange(self, nums: List[int], target: int) -> List[int]:
#         lower = self.findLowerBound(nums, target)
#         if lower == -1:
#             return [-1, -1]

#         upper = self.findUpperBound(nums, target)

#         return [lower, upper]

#     def findLowerBound(self, nums: List[int], target: int) -> int:
#         left, right = 0, len(nums)

#         while left < right:
#             mid = (left + right) // 2

#             if nums[mid] < target: # ⭐️
#                 left = mid + 1
#             else:
#                 right = mid

#         if left < len(nums) and nums[left] == target: # ⭐️
#             return left # ⭐️
#         else:
#             return -1

#     def findUpperBound(self, nums: List[int], target: int) -> int:
#         left, right = 0, len(nums)

#         while left < right:
#             mid = (left + right) // 2

#             if nums[mid] <= target:  # ⭐️
#                 left = mid + 1
#             else:
#                 right = mid

#         if left > 0 and nums[left - 1] == target:  # ⭐️
#             return left - 1  # ⭐️
#         else:
#             return -1

s = Solution()
input_ = [2, 2]
target = 3
result = s.searchRange(input_, target)
print(result)
