"""
📌 信号→模式: s 的子序列等于 t 的个数 → 双序列 DP：相等 take + skip，不等 skip；j == n → 1
📅 首次: 2026-09-05 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 2026-09-05 🟡 | 下次: 2026-09-08
"""
from functools import lru_cache


class Solution_1_Recursive:
    def numDistinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)

        @lru_cache(maxsize=None)
        def dp(i: int, j: int) -> int:
            if j == n:  # t 匹配完 → 成功，1 种（s 剩多少都不选）
                return 1
            if m - i < n - j:  # s 剩的不够 t 用 → 必败（可选剪枝，含 i==m 情形）
                return 0
            if s[i] == t[j]:
                return dp(i + 1, j + 1) + dp(i + 1, j)  # 配对 / 不配对这个 s[i]
            return dp(i + 1, j)  # 不等只能跳过 s[i]

        return dp(0, 0)


class Solution_2_Iterative:
    def numDistinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][n] = 1
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                dp[i][j] += dp[i + 1][j]
                if s[i] == t[j]:
                    dp[i][j] += dp[i + 1][j + 1]
        return dp[0][0]


s = Solution_1_Recursive()
s_ = "aaat"
t_ = "at"
# s_ = "caaat"
# t_ = "cat"
result = s.numDistinct(s_, t_)
print(result)
