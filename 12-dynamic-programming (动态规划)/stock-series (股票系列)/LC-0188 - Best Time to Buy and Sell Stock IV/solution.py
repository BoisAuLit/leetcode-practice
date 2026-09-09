"""LC-0188 - Best Time to Buy and Sell Stock IV

合并自 2 个解法文件:
  1. 13 - 0188 - A - Buy Sell Stock IV - Top Down Memoization - 3D-DP - 🐢🐢🐢.py
  2. 13 - 0188 - B - Buy Sell Stock IV - Bottom Up Iteration - 3D-DP - 🚀🚀🚀.py
"""

from typing import List

from functools import cache


# ============================================================================
# Solution 1: Top_Down_Memoization    (原文件: 13 - 0188 - A - Buy Sell Stock IV - Top Down Memoization - 3D-DP - 🐢🐢🐢.py)
# ============================================================================

class Solution_1_Top_Down_Memoization:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)
        # States:
        # 1. Holding or not (0 means not holding, 1 means holding)
        # 2. i (index currently being processed)
        # 3. transactions already made (decides if we can continue or not)

        # Only when we sell will we decrease remain by 1
        @cache
        def dp(i: int, holding: int, remain: int) -> int:
            if i >= n or remain == 0:
                return 0
            do_nothing = dp(i + 1, holding, remain)
            if holding:
                return max(prices[i] + dp(i + 1, 0, remain - 1), do_nothing)
            else:
                return max(-prices[i] + dp(i + 1, 1, remain), do_nothing)

        return dp(0, 0, k)

# ============================================================================
# Solution 2: Bottom_Up_Iteration    (原文件: 13 - 0188 - B - Buy Sell Stock IV - Bottom Up Iteration - 3D-DP - 🚀🚀🚀.py)
# ============================================================================

class Solution_2_Bottom_Up_Iteration:
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
