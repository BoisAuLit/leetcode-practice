from typing import List
from functools import cache


class Solution:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        n = len(nums)
        m = len(multipliers)
        dp = [0] * (m + 1)
        # ! Initialize the first dp array
        for i in range(1, m + 1):
            dp[i] = dp[i - 1] + nums[n - i] * multipliers[i - 1]
        # ! Initialize the maximum value
        max_ = dp[-1]
        for i in range(1, m + 1):
            # ! dp[0] means only take numbers on left side
            dp[0] += nums[i - 1] * multipliers[i - 1]
            for j in range(1, m - i + 1):
                k = i + j - 1
                dp[j] = max(
                    nums[i - 1] * multipliers[k] + dp[j],  # Take from left
                    nums[n - j] * multipliers[k] + dp[j - 1],  # Take from right
                )
                if i + j == m:
                    max_ = max(max_, dp[j])
        return max_



# s = Solution()
# nums = [-5, -3, -3, -2, 7, 1]
# multipliers = [-10, -5, 3, 4, 6]
# result = s.maximumScore(nums, multipliers)
# print(result)
