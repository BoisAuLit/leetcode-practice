from typing import List
from functools import lru_cache


class Solution_1:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)

        @lru_cache
        def dp(i):
            if i >= n - 2:
                return cost[i]
            return cost[i] + min(dp(i + 1), dp(i + 2))

        return min(dp(0), dp(1))


class Solution_2:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        dp = [0] * len(cost)
        dp[n - 1], dp[n - 2] = cost[n - 1], cost[n - 2]
        for i in range(n - 3, -1, -1):
            dp[i] = cost[i] + min(dp[i + 1 : i + 3])
        return min(dp[:2])


class Solution_3:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        a, b = cost[-2:]
        for i in range(n - 3, -1, -1):
            a, b = cost[i] + min(a, b), a
        return min(a, b)


s = Solution_3()
cost = [1, 2, 3]
result = s.minCostClimbingStairs(cost)
print(result)
