from typing import List


class Solution:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        n = len(nums)
        m = len(multipliers)
        dp = [[0] * (m + 1) for _ in range(m + 1)]
        max_ = float("-inf")
        for i in range(1, m + 1):
            dp[0][i] = dp[0][i - 1] + nums[n - i] * multipliers[i - 1]
            dp[i][0] = dp[i - 1][0] + nums[i - 1] * multipliers[i - 1]
            if i == m:
                max_ = max(max_, dp[0][i], dp[i][0])

        for i in range(1, m + 1):
            for j in range(1, m + 1 - i):
                k = i + j - 1
                dp[i][j] = max(
                    # Take one from left
                    dp[i - 1][j] + multipliers[k] * nums[i - 1],
                    # Take one from right
                    dp[i][j - 1] + multipliers[k] * nums[n - j],
                )
                if i + j == m:
                    max_ = max(max_, dp[i][j])
        return max_


# s = Solution()
# nums = [-5, -3, -3, -2, 7, 1]
# multipliers = [-10, -5, 3, 4, 6]
# result = s.maximumScore(nums, multipliers)
# print(result)
