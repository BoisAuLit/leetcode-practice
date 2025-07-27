from typing import List
from functools import lru_cache


class Solution_Top_Donw_Memoization:
    def coinChange(self, coins: List[int], amount: int) -> int:

        @lru_cache(None)
        def dfs(rem):
            if rem < 0:
                return -1
            if rem == 0:
                return 0
            min_cost = float('inf')
            for coin in coins:
                res = dfs(rem - coin)
                if res != -1:
                    min_cost = min(min_cost, res + 1)
            return min_cost if min_cost != float('inf') else -1

        return dfs(amount)


class Solution_Bottom_Up_Perfect_Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        
        for coin in coins:
            for x in range(coin, amount + 1):
                dp[x] = min(dp[x], dp[x - coin] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1 


# s = Solution()
# coins = [1]
# amount = 0
# result = s.coinChange(coins, amount)
# print(result)


# s = Solution()
# coins = [1, 2, 5]
# amount = 11
# result = s.coinChange(coins, amount)
# print(result)

# s = Solution()
# coins = [2]
# amount = 3
# result = s.coinChange(coins, amount)
# print(result)
