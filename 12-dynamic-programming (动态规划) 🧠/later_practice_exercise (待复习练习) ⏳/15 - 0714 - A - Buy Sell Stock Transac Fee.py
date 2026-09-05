from typing import List
from functools import lru_cache

class Solution_Top_Down_Memoization:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        n = len(prices)

        @lru_cache
        def dp(i: int, holding: int) -> int:
            if i >= n:
                return 0
            if holding:
                return max(dp(i + 1, 1), prices[i] - fee + dp(i + 1, 0))
            return max(dp(i + 1, 0), -prices[i] + dp(i + 1, 1))

        return dp(0, 0)


class Solution_Bottom_Up_Iteration:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        n = len(prices)
        # 1st item: From index 0 to index i, if not holding at index i
        # 2nd item: From index 0 to index i, if holding at index i
        dp = [0, -prices[0]]
        for i in range(1, n):
            not_holding = max(dp[0], dp[1] + prices[i] - fee)
            holding = max(dp[1], dp[0] - prices[i])
            dp = [not_holding, holding]

        return max(dp)


# s = Solution()
# prices = [1, 3, 2, 8, 4, 9]
# fee = 2
# result = s.maxProfit(prices, fee)
# print(result)
