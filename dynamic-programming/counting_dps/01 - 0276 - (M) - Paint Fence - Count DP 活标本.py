from functools import lru_cache


class Solution_Bottom_Up_Memoization:
    def numWays(self, n: int, k: int) -> int:
        if n <= 2:
            return k**n

        @lru_cache(None)
        def dp(i: int, two_same: int) -> int:
            if i == n:  # ! Take note of this base case
                return k - 1 if two_same else k
            if i == 1:  # ! Take note of this special case
                return k * (k - 1) * dp(3, 0) + k * dp(3, 1)
            if two_same:
                return (k - 1) * dp(i + 1, 0)
            return dp(i + 1, 1) + (k - 1) * dp(i + 1, 0)

        return dp(1, 0)


class Solution_Bottom_Up_Iteration:
    def numWays(self, n: int, k: int) -> int:
        if n <= 2:
            return k**n

        dp = [[0] * 2 for _ in range(n)]

        """
        dp[i][0] means it's the same color as previous one
        dp[i][1] means current color is different from previous one
        """
        dp[0] = [0, k]
        for i in range(1, n):
            dp[i][0] = dp[i - 1][1]
            dp[i][1] = (k - 1) * sum(dp[i - 1])

        return sum(dp[-1])


# s = Solution()

# n = 7
# k = 2
# # n = 2
# # k = 1
# result = s.numWays(n, k)
# print(result)
