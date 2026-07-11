from functools import lru_cache

path = "../../assets/0062_Unique_Paths.jpeg"


class Solution_Top_Down_Memoization:
    def uniquePaths(self, m: int, n: int) -> int:
        @lru_cache(None)
        def dp(x: int, y: int) -> int:
            if x == m - 1 and y == n - 1:
                return 1
            if x >= m or y >= n:
                return 0
            return dp(x + 1, y) + dp(x, y + 1)

        return dp(0, 0)


class Solution_Bottom_Up_Iteration:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[0] * n for _ in range(m)]
        for i in range(m):
            dp[i][-1] = 1
        for i in range(n):
            dp[-1][i] = 1
        for j in range(n - 2, -1, -1):
            for i in range(m - 2, -1, -1):
                dp[i][j] = dp[i + 1][j] + dp[i][j + 1]
        return dp[0][0]


class Solution_Bottom_Up_Iteration_Space_Optimized:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * m
        # ! The outer loop variable is not important so we use underscore
        for _ in range(n - 2, -1, -1):
            for i in range(m - 2, -1, -1):
                """
                When we compute new dp[i], its right and bottom are already calculated
                Right = p[i] (previously calculated)
                Bottom = dp[i+1] (preiously calculated)
                """
                dp[i] += dp[i + 1]
        return dp[0]


# s = Solution()
# m = 3
# n = 7
# result = s.uniquePaths(m, n)
# print(result)
