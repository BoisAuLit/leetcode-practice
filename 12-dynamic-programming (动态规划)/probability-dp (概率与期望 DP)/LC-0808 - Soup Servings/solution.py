"""LC-0808 - Soup Servings

合并自 2 个解法文件:
  1. 01 - 0808 - A - Soup Servings - Bottom Up Iteration.py
  2. 01 - 0808 - B - Soup Servings - Top Down Memo.py
"""

from math import ceil

from functools import cache


# ============================================================================
# Solution 1: Bottom_Up_Iteration    (原文件: 01 - 0808 - A - Soup Servings - Bottom Up Iteration.py)
# ============================================================================

n_1 = 100

class Solution_1_Bottom_Up_Iteration:
    def soupServings(self, n_1: int) -> float:
        m = ceil(n_1 / 25)
        dp = {}

        def calculate_dp(i, j):
            return (
                dp[max(0, i - 4)][j]
                + dp[max(0, i - 3)][j - 1]
                + dp[max(0, i - 2)][max(0, j - 2)]
                + dp[i - 1][max(0, j - 3)]
            ) / 4

        dp[0] = {0: 0.5}
        for k in range(1, m + 1):
            dp[0][k] = 1
            dp[k] = {0: 0}
            for j in range(1, k + 1):
                dp[j][k] = calculate_dp(j, k)
                dp[k][j] = calculate_dp(k, j)
            if dp[k][k] > 1 - 1e-5:
                return 1
        return dp[m][m]

# ============================================================================
# Solution 2: Top_Down_Memo    (原文件: 01 - 0808 - B - Soup Servings - Top Down Memo.py)
# ============================================================================

n_2 = 100

class Solution_2_Top_Down_Memo:
    def soupServings(self, n_2: int) -> float:
        m = ceil(n_2 / 25)

        @cache
        def dp(i: int, j: int) -> float:
            if i <= 0 and j <= 0:
                return 0.5
            if i <= 0:
                return 1.0
            if j <= 0:
                return 0.0

            return (
                dp(i - 4, j)
                + dp(i - 3, j - 1)
                + dp(i - 2, j - 2)
                + dp(i - 1, j - 3)
            ) / 4.0

        # This is very imporant to avoid stack overflow!
        for k in range(1, m + 1):
            if dp(k, k) > 1 - 1e-5:
                return 1.0
        return dp(m, m)


if __name__ == "__main__":

    # --- Solution 1: Bottom_Up_Iteration ---
    s = Solution_1_Bottom_Up_Iteration()
    result = s.soupServings(n_1)
    print(result)

    # --- Solution 2: Top_Down_Memo ---
    s = Solution_2_Top_Down_Memo()
    result = s.soupServings(n_2)
    print(result)
