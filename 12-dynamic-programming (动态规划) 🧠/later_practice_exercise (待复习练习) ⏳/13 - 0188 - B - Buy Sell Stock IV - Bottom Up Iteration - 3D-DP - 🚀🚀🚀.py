from typing import List


class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)
        # ! ⚠️ Caveats 1: To make 3D array, we need two nested levels of list comphrehension
        dp = [[[float("-inf")] * 2 for j in range(k + 1)] for i in range(n)]

        """
        ! [Not holding, holding]
        ! Only when we sell a stock will we finish a transaction and decrease k by 1
        """
        dp[0][-1] = [0, -prices[0]]
        # ! ⚠️ Caveats 2: Initial value of max_ MUST be zero !
        max_ = 0
        for i in range(1, n):
            for j in range(k, -1, -1):
                dp[i][j][0] = max(
                    # Previously not holding, today do nothing (keep not holding)
                    dp[i - 1][j][0],
                    # Previously holding, now sell it (sell stock today)
                    dp[i - 1][j + 1][1] + prices[i]
                    if j + 1 <= k
                    else float("-inf"),
                )
                dp[i][j][1] = max(
                    # Previously holding, today do nothing (keep holding)
                    dp[i - 1][j][1],
                    # Previously not holding, now buy it (buy stock today)
                    dp[i - 1][j][0] - prices[i],
                )
                max_ = max(max_, dp[i][j][0], dp[i][j][1])
        print()
        return max_


# s = Solution()
# k = 2
# prices = [3, 2, 6, 5, 0, 3]
# result = s.maxProfit(k, prices)
# print(result)
