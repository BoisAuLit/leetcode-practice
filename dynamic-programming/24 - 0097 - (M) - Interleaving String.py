from functools import cache

path = "../assets/0097 - Interleaving string.pdf"
video = "https://www.youtube.com/watch?v=3Rw3p9LrgvE"

class Solution_Top_Down_Memoization:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        n = len(s1)
        m = len(s2)
        if n + m != len(s3):
            return False

        @cache
        def dp(i: int, j: int) -> bool:
            # If both i & j are out of bound, then we finished with success
            if i == n and j == m:
                return True
            if i < n and s1[i] == s3[i + j] and dp(i + 1, j):
                return True
            if j < m and s2[j] == s3[i + j] and dp(i, j + 1):
                return True
            return False

        return dp(0, 0)


class Solution_Bottom_Up_Iteration:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        n = len(s1)
        m = len(s2)
        if n + m != len(s3):
            return False

        dp = [[False] * (m + 1) for _ in range(n + 1)]
        dp[-1][-1] = True
        for i in range(n, -1, -1):
            for j in range(m, -1, -1):
                if i < n and s1[i] == s3[i + j] and dp[i + 1][j]:
                    dp[i][j] = True
                if j < m and s2[j] == s3[i + j] and dp[i][j + 1]:
                    dp[i][j] = True
        return dp[0][0]


s = Solution_Bottom_Up_Iteration()
s1 = "aabcc"
s2 = "dbbca"
s3 = "aadbbcbcac"
result = s.isInterleave(s1, s2, s3)
print(result)
