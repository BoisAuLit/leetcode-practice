class Solution:
    """
    n --> 目标和
    x --> 幂次
    """
    def numberOfWays(self, n: int, x: int) -> int:
        MOD = 10**9 + 7

        """
        dp[i][j]: 用 1 到 i 这些整数的 x 次方，凑出 j 的方案数
        """
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for i in range(1, n + 1):
            val = i**x
            for j in range(n + 1):
                dp[i][j] = dp[i - 1][j]
                if j >= val:
                    dp[i][j] = (dp[i][j] + dp[i - 1][j - val]) % MOD
        return dp[n][n]

