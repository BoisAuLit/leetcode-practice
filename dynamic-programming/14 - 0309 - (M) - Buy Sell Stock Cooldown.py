from typing import List
from functools import lru_cache
import math


class Solution_Top_Down_Memoization:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)

        @lru_cache(None)
        def dp(i: int, holding: int) -> int:
            if i >= n:
                return 0
            do_nothing = dp(i + 1, holding)

            if holding:
                do_something = prices[i] + dp(i + 2, 0)
            else:
                do_something = -prices[i] + dp(i + 1, 1)
            return max(do_something, do_nothing)

        return dp(0, 0)


class Solution_Bottom_Up_Iteration_Very_Efficient:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        if n == 1:
            return 0

        """
        Every inner array (of size 3) represents 3 states:
        dp[i][0] -> holding a stock
        dp[i][1] -> not holding a stock (but cooldown) (means just sold a stock on that day)
        dp[i][2] -> not holding, not cooldown
        """
        dp = [[0] * 3 for _ in range(n)]
        dp[0] = [-prices[0], -math.inf, 0]
        for i in range(1, n):
            price = prices[i]
            dp[i][0] = max(dp[i - 1][0], dp[i - 1][2] - price)
            dp[i][1] = dp[i - 1][0] + price
            dp[i][2] = max(dp[i - 1][1], dp[i - 1][2])

        return max(dp[-1])



# s = Solution()
# prices = [1, 2, 3, 0, 2]
# result = s.maxProfit(prices)
# print(result)
