from typing import List
from functools import lru_cache


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        n = len(coins)
        @lru_cache(maxsize=None)
        def dp(i: int, remain: int) -> int:
            if remain < 0:
                return float("inf")      # 这条路扣超了，判死这一条路
            if remain == 0:
                return 0
            if i == n:
                return float("inf")
            take = 1 + dp(i, remain - coins[i])
            skip = dp(i + 1, remain)
            return min(take, skip)

        res = dp(0, amount)
        return res if res != float("inf") else -1


class Solution_2:
    def coinChange(self, coins: List[int], amount: int) -> int:
        n = len(coins)
        dp = [[float("inf")] * (amount + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = 0
        for i in range(n - 1, -1, -1):
            for remain in range(1, amount+1):
                take = 1 + dp[i][remain - coins[i]] if remain - coins[i] >= 0 else float("inf")
                skip = dp[i + 1][remain]
                dp[i][remain] = min(take, skip)
        return dp[0][amount] if dp[0][amount] != float("inf") else -1


s = Solution_2()
coins = [1, 2, 5]
amount = 11
result = s.coinChange(coins, amount)
print(result)
