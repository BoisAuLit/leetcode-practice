from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        coins.sort()

        dp = [float("inf")] * (amount + 1)
        dp[0] = 0

        for curr_amount in range(1, amount + 1):
            for coin in coins:
                if coin > curr_amount:
                    break

                dp[curr_amount] = min(dp[curr_amount], 1 + dp[curr_amount - coin])

        return dp[amount] if dp[amount] != float("inf") else -1


s = Solution()
coins = [1, 5, 10]
amount = 12
result = s.coinChange(coins, amount)
print(result)
