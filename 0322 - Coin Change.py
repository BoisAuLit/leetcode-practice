from typing import List
from functools import lru_cache
import math


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        min_coin = min(coins)
        coins_set = set(coins)
        if amount == 0:
            return 0

        @lru_cache(maxsize=None)
        def dfs(amount):
            if amount < 0 or amount < min_coin:
                return math.inf
            if amount in coins_set:
                return 1
            return 1 + min(dfs(amount - coin) for coin in coins)

        result = dfs(amount)
        if result == math.inf:
            return -1
        return result


s = Solution()


# coins = [1]
# amount = 0
# coins = [2]
# amount = 3

coins = [1, 2, 5]
amount = 11
result = s.coinChange(coins, amount)
print(result)
