from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        # hold, sold, free
        dp = [[float("-inf")] * n for _ in range(3)]
        dp[0][0] = -prices[0]
        dp[2][0] = 0
        for j in range(1, n):
            dp[0][j] = max(dp[0][j - 1], dp[2][j - 1] - prices[j])
            dp[1][j] = dp[0][j - 1] + prices[j]
            dp[2][j] = max(dp[1][j - 1], dp[2][j - 1])
        return max(dp[i][-1] for i in range(3))


s = Solution()
input_ = [1, 3, 4, 0, 4]
result = s.maxProfit(input_)
print(result)
