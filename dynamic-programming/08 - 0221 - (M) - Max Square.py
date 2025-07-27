class Solution_Bottom_Up_1:
    def maximalSquare(self, matrix):
        m = len(matrix)
        n = len(matrix[0])
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        maxsqlen = 0
        # for convenience, we add an extra all zero column and row
        # outside of the actual dp table, to simpify the transition
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if matrix[i - 1][j - 1] == "1":
                    dp[i][j] = (
                        min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1]) + 1
                    )
                    maxsqlen = max(maxsqlen, dp[i][j])
        return maxsqlen * maxsqlen


class Solution_Bottom_Up_2_Optimized:
    def maximalSquare(self, matrix):
        m = len(matrix)
        n = len(matrix[0])
        dp = [0] * (n + 1)
        maxsqlen = 0
        prev = 0
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                temp = dp[j]
                if matrix[i - 1][j - 1] == "1":
                    dp[j] = min(dp[j - 1], prev, dp[j]) + 1
                    maxsqlen = max(maxsqlen, dp[j])
                else:
                    dp[j] = 0
                prev = temp
        return maxsqlen * maxsqlen
