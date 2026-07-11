from functools import lru_cache
from typing import List

class Solution_DP_Bottom_Up_Iteration:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        dp = [0] * (n+1)
        for i in range(2, n+1):
            dp[i] = min(
                dp[i-2] + cost[i-2],
                dp[i-1] + cost[i-1]
            )
        return dp[-1]

class Solution_DP_Top_Down_Memoization:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        @lru_cache(None)
        def dp(i: int) -> int:
            if i < 2:
                # ! 注意，这里特别容易出错！
                return cost[i]
            return min(
                dp(i-2) + cost[i-2],
                dp(i-1) + cost[i-1]
            )
        return dp(len(cost))
            