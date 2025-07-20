from typing import List


class Solution_Bottom_Up_Iteration_Faster:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        dp = [0] * n
        dp[-1], dp[-2] = cost[-1], cost[-2]
        for i in range(n - 3, -1, -1):
            dp[i] = cost[i] + min(dp[i + 1], dp[i + 2])
        return min(dp[0], dp[1])


class Solution_Top_Down_Memoization_Slower:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        def dp(i: int) -> int:
            if i >= n-2:
                return cost[i]
            if i not in memo:
                memo[i] = cost[i] + min(dp(i+1), dp(i+2))
            return memo[i]
        memo = {}
        return min(dp(0), dp(1))


