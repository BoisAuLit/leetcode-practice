from typing import List


class Solution_Top_Down_Memoization:
    def change(self, amount: int, coins: List[int]) -> int:
        """
        numberOfWays(i, amount) means
        The number of ways to make up amount only using coins
        starting form index i
        """

        def numberOfWays(i: int, amount: int) -> int:
            if amount == 0:
                return 1
            if i == len(coins):
                return 0
            if memo[i][amount] != -1:
                return memo[i][amount]

            if coins[i] > amount:
                memo[i][amount] = numberOfWays(i + 1, amount)
            else:
                memo[i][amount] = numberOfWays(
                    i, amount - coins[i]
                ) + numberOfWays(i + 1, amount)

            return memo[i][amount]

        memo = [[-1] * (amount + 1) for _ in range(len(coins))]
        return numberOfWays(0, amount)


class Solution_Bottom_Up_Iteration:
    def change(self, amount: int, coins: List[int]) -> int:
        n = len(coins)
        """
        dp[i][amount] means
        The number of ways to make up amount only using coins 
        starting form index i
        """
        dp = [[0] * (amount + 1) for _ in range(n + 1)]

        # We initialize dp[i][0] to 1 as it's awalys possible
        # to make up 0 amount with any coin
        for i in range(n):
            dp[i][0] = 1

        for i in range(n - 1, -1, -1):
            for j in range(1, amount + 1):
                if coins[i] > j:
                    dp[i][j] = dp[i + 1][j]
                else:
                    dp[i][j] = dp[i + 1][j] + dp[i][j - coins[i]]

        return dp[0][amount]


class Solution_Bottom_Up_Iteration_Space_Optimized:
    def change(self, amount: int, coins: List[int]) -> int:
        n = len(coins)
        """
        dp[i][amount] means
        The number of ways to make up amount only using coins 
        starting form index i
        """
        dp = [0] * (amount + 1)
        # We initialize dp[0] to 1 as it's awalys possible
        # to make up 0 amount with any coin
        dp[0] = 1

        for i in range(n - 1, -1, -1):
            for j in range(coins[i], amount + 1):
                dp[j] += dp[j - coins[i]]

        return dp[amount]
