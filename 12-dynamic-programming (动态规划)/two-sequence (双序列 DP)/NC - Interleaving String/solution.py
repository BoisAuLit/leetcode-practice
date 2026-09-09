from functools import lru_cache


class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m = len(s1)
        n = len(s2)
        if m + n != len(s3):
            return False

        @lru_cache(maxsize=None)
        def dp(i: int, j: int) -> bool:
            if i == m:
                return s2[j:] == s3[i + j :]
            if j == n:
                return s1[i:] == s3[i + j :]
            a, b, c = s1[i], s2[j], s3[i + j]
            if c not in [a, b]:
                return False
            elif a == c and b != c:
                return dp(i + 1, j)
            elif a != c and b == c:
                return dp(i, j + 1)
            else:
                return dp(i + 1, j) or dp(i, j + 1)

        return dp(0, 0)


class Solution_2:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m = len(s1)
        n = len(s2)
        if m + n != len(s3):
            return False
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[m][n] = True
        for j in range(n - 1, -1, -1):
            if s2[j] != s3[-(n - j)]:
                break
            dp[m][j] = True
        for i in range(m - 1, -1, -1):
            if s1[i] != s3[-(m - i)]:
                break
            dp[i][n] = True

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                a, b, c = s1[i], s2[j], s3[i + j]
                if c not in [a, b]:
                    continue
                elif a == c and b != c:
                    dp[i][j] = dp[i + 1][j]
                elif a != c and b == c:
                    dp[i][j] = dp[i][j + 1]
                else:
                    dp[i][j] = dp[i + 1][j] or dp[i][j + 1]

        return dp[0][0]


s = Solution()

# s1 = "aaaa"
# s2 = "bbbb"
# s3 = "aabbbbaa"

# s1 = "abc"
# s2 = "xyz"
# s3 = "abxzcy"

s1 = "ba"
s2 = "c"
s3 = "cbx"

result = s.isInterleave(s1, s2, s3)
print(result)
