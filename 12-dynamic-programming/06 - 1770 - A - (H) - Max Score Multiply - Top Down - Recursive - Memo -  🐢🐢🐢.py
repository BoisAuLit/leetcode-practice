from typing import List
from functools import cache


class Solution:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        @cache
        def dp(l: int, r: int) -> int:
            # ! l --> left pointer in nums
            # ! r --> right pointer in nums (not taking how many from right side)
            m = l + len(nums) - 1 - r
            if m >= len(multipliers):
                return 0

            return max(
                nums[l] * multipliers[m] + dp(l + 1, r),
                nums[r] * multipliers[m] + dp(l, r - 1),
            )

        return dp(0, len(nums) - 1)


# s = Solution()
# nums = [-5, -3, -3, -2, 7, 1]
# multipliers = [-10, -5, 3, 4, 6]
# result = s.maximumScore(nums, multipliers)
# print(result)
