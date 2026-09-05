from typing import List
from functools import lru_cache


class Solution_Top_Down_Memoization:
    def minCost(self, costs: List[List[int]]) -> int:
        n = len(costs)

        @lru_cache(None)
        def dp(i: int, j: int) -> int:
            if i == n - 1:
                return costs[i][j]
            return costs[i][j] + min(dp(i + 1, x) for x in [0, 1, 2] if x != j)

        return min(dp(0, 0), dp(0, 1), dp(0, 2))


class Solution_Bottom_Up_Iteration:
    def minCost(self, costs: List[List[int]]) -> int:
        # 1st item: From index 0 to index i, if choosing red at index i
        # 2st item: From index 0 to index i, if choosing blue at index i
        # 3rd item: From index 0 to index i, if choosing green at index i
        dp = costs[0]
        for i in range(1, len(costs)):
            temp = [0] * 3
            for j in range(3):
                temp[j] = costs[i][j] + min(dp[x] for x in range(3) if x != j)
            dp = temp
        return min(dp)
        


# s = Solution()
# costs = [[17, 2, 17], [16, 16, 5], [14, 3, 19]]
# result = s.minCost(costs)
# print(result)
