from typing import List
from functools import cache


class Solution_Top_Down_Memoization:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        n = len(multipliers)

        @cache
        def dp(p1: int, p2: int, i: int) -> int:
            mult = multipliers[i]
            if i == n - 1:
                return max(mult * nums[p1], mult * nums[p2])
            return max(
                nums[p1] * mult + dp(p1 + 1, p2, i + 1),
                nums[p2] * mult + dp(p1, p2 - 1, i + 1),
            )

        return dp(0, len(nums) - 1, 0)



class Solution_Bottom_Up_Iteration:
    explanation = "../assets/1170_DP_Bottom_Up.jpeg"    
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        m = len(multipliers)
        dp = [[0] * (m + 1) for i in range(m + 1)]
        max_ = float("-inf")
        for i in range(m):
            dp[0][i + 1] = dp[0][i] + nums[-(i + 1)] * multipliers[i]
            dp[i + 1][0] = dp[i][0] + nums[i] * multipliers[i]
            if i == m:
                max_ = max(dp[0][i + 1], dp[i + 1][0])

        for i in range(1, m):
            for j in range(1, 1 + (m - i)):
                dp[i][j] = max(
                    dp[i - 1][j] + nums[i - 1] * multipliers[i + j - 1],
                    dp[i][j - 1] + nums[-j] * multipliers[i + j - 1],
                )
                if i + j == m:
                    max_ = max(max_, dp[i][j])

        return max_


# s = Solution()
# nums = [-5, -3, -3, -2, 7, 1]
# multipliers = [-10, -5, 3, 4, 6]
# result = s.maximumScore(nums, multipliers)
# print(result)
