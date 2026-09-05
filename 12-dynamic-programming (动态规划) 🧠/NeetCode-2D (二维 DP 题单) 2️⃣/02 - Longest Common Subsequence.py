from functools import cache

# ! Easiest: Top Down Memoization
class Solution_1:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m = len(text1)
        n = len(text2)
        @cache
        def dp(i: int, j: int) -> int:
            if i == m-1:
                return int(text1[-1] in text2[j:])
            if j == n-1:
                return int(text2[-1] in text1[i:])
            return max(
                dp(i, j+1),
                dp(i+1, j),
                dp(i+1, j+1) + int(text1[i] == text2[j])
            )
        return dp(0, 0)

# ! Bottom up Iteration (without space optimization)
# ! ⭐️⭐️⭐️ This is the preferred solution
class Solution_2:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m = len(text1)
        n = len(text2)
        dp = [[0] * n for _ in range(m)]
        dp[0][0] = int(text1[0] == text2[0])
        for i in range(1, n):
            dp[0][i] = int(text2[i] == text1[0] or dp[0][i-1])
        for i in range(1, m):
            dp[i][0] = int(text1[i] == text2[0] or dp[i-1][0])
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = max(
                    dp[i-1][j],
                    dp[i][j-1],
                    dp[i-1][j-1] + int(text1[i] == text2[j])
                )
        return dp[-1][-1]

# ! Bottom up Iteration (with space optimization)
class Solution_3:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m = len(text1)
        n = len(text2)
        dp = [0] * n
        dp[0] = int(text1[0] == text2[0])
        for i in range(1, n):
            dp[i] = int(text2[i] == text1[0] or dp[i-1])
        for i in range(1, m):
            new_dp = [0] * n
            new_dp[0] = int(text1[i] == text2[0] or dp[0])
            for j in range(1, n):
                new_dp[j] = max(
                    dp[j],
                    new_dp[j-1],
                    dp[j-1] + int(text1[i] == text2[j])
                )
            dp = new_dp
        return dp[-1]
