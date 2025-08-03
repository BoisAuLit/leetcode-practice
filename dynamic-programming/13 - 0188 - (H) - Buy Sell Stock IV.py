import math
from typing import List
from functools import lru_cache


class Solution_Top_Down_Not_Efficient:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        @lru_cache(None)
        def dp(i, transactions_remaining, holding):
            # Base case
            if transactions_remaining == 0 or i == len(prices):
                return 0

            do_nothing = dp(i + 1, transactions_remaining, holding)

            if holding:
                # Sell stock
                do_something = prices[i] + dp(
                    i + 1, transactions_remaining - 1, 0
                )
            else:
                # Buy stock
                do_something = -prices[i] + dp(i + 1, transactions_remaining, 1)

            # Recurrence relation
            return max(do_nothing, do_something)

        return dp(0, k, 0)


class Solution_Bottom_Up_Efficient:
    """
    Explanation: "../assets/0188. Best Time to Buy and Sell Stock IV.pdf"
    """
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)

        # solve special cases
        if not prices or k == 0:
            return 0

        if k * 2 >= n:
            res = 0
            for i, j in zip(prices[1:], prices[:-1]):
                res += max(0, i - j)
            return res

        # dp[i][used_k][ishold] = balance
        # ishold: 0 nothold, 1 hold
        dp = [[[-math.inf] * 2 for _ in range(k + 1)] for _ in range(n)]

        # set starting value
        dp[0][0][0] = 0
        dp[0][1][1] = -prices[0]

        # fill the array
        for i in range(1, n):
            for j in range(k + 1):
                # transition equation
                dp[i][j][0] = max(dp[i - 1][j][0], dp[i - 1][j][1] + prices[i])
                # you can't hold stock without any transaction
                if j > 0:
                    dp[i][j][1] = max(
                        dp[i - 1][j][1], dp[i - 1][j - 1][0] - prices[i]
                    )

        res = max(dp[n - 1][j][0] for j in range(k + 1))
        return res


# s = Solution()
# k = 2
# prices = [3, 2, 6, 5, 0, 3]
# result = s.maxProfit(k, prices)
# print(result)
