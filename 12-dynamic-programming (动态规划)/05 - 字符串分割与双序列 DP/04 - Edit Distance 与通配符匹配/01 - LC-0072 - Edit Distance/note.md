# Edit Distance 笔记

### 📝 2026-10-26 - retry 1

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)

        @lru_cache(maxsize=None)
        def dp(i: int, j: int) -> int:
            if i == m:
                return n - j
            if j == n:
                return m - i
            if word1[i] == word2[j]:
                return dp(i + 1, j + 1)
            return 1 + min(
                dp(i, j + 1),  # Insert before i
                dp(i + 1, j + 1),  # Replace at i
                dp(i + 1, j),  # Delete at i
            )

        return dp(0, 0)

    def minDistance_iter(self, word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for j in range(n + 1):
            dp[m][j] = n - j
        for i in range(m + 1):
            dp[i][n] = m - i
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if word1[i] == word2[j]:
                    dp[i][j] = dp[i + 1][j + 1]
                else:
                    dp[i][j] = 1 + min(dp[i][j + 1], dp[i + 1][j + 1], dp[i + 1][j])
        return dp[0][0]
```
