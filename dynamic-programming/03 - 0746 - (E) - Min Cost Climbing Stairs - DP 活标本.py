from typing import List
from functools import lru_cache

class Solution_Bottom_Up_Very_Inefficient:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)

        @lru_cache(None)
        def dp(i: int) -> int:
            if i >= n:
                return 0
            return cost[i] + min(dp(i + 1), dp(i + 2))

        return min(dp(0), dp(1))


class Solution_Very_Efficient:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)

        x = cost[-2]
        y = cost[-1]
        for i in range(n - 3, -1, -1):
            curr = cost[i] + min(x, y)
            x, y = curr, x
        return min(x, y)

