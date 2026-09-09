"""LC-2787 - Ways to Express an Integer as Sum of Powers

合并自 5 个解法文件:
  1. 26 - 2787 - A - Ways to Express Int as Sum of Powers.py
  2. 28 - 2787 - A - Ways to Express Integer Sum Power - Top Down Memo.py
  3. 28 - 2787 - A - Ways to Express Integer Sum Powers 🐢.py
  4. 28 - 2787 - B - Ways to Express Integer Sum Power - Bottom Up 🚀.py
  5. 28 - 2787 - C - Ways to Express Integer Sum Power - Bottom Up Space Optimized 🚀🚀🚀.py
"""

from functools import cache

from pprint import pprint

import math


# ============================================================================
# Solution 1: Ways_to_Express_Int_as_Sum_of_Powers    (原文件: 26 - 2787 - A - Ways to Express Int as Sum of Powers.py)
# ============================================================================

class Solution_1_Ways_to_Express_Int_as_Sum_of_Powers:
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

# ============================================================================
# Solution 2: Top_Down_Memo    (原文件: 28 - 2787 - A - Ways to Express Integer Sum Power - Top Down Memo.py)
# ============================================================================

n_2 = 4

x_2 = 1

class Solution_2_Top_Down_Memo:
    def numberOfWays(self, n_2: int, x_2: int) -> int:
        mod = 10**9 + 7

        @cache
        def dp(i: int, remain: int) -> int:
            val = i**x_2
            if val == remain:
                return 1
            elif val > remain:
                return 0
            return (
                dp(i + 1, remain - val) % mod + dp(i + 1, remain) % mod
            ) % mod

        return dp(1, n_2)

# ============================================================================
# Solution 3: Ways_to_Express_Integer_Sum_Powers    (原文件: 28 - 2787 - A - Ways to Express Integer Sum Powers 🐢.py)
# ============================================================================

# ============================================================================
# Solution 4: Bottom_Up    (原文件: 28 - 2787 - B - Ways to Express Integer Sum Power - Bottom Up 🚀.py)
# ============================================================================

n_4 = 4

x_4 = 1

class Solution_4_Bottom_Up:
    def numberOfWays(self, n_4: int, x_4: int) -> int:
        mod = 10**9 + 7
        dp = [[0] * (n_4 + 1) for _ in range(n_4 + 1)]

        # Here use math.ceil because 64**(1/3) = 3.9xx6 (not 4)
        root = math.ceil(n_4 ** (1/x_4))
        val = root**x_4
        if 1 <= val <= n_4:
            dp[root][val] = 1

        for i in range(root - 1, 0, -1):
            pow = i**x_4
            for remain in range(1, n_4 + 1):
                if pow < remain:
                    dp[i][remain] = (
                        dp[i + 1][remain - pow] + dp[i + 1][remain]
                    ) % mod
                elif pow == remain:
                    dp[i][remain] = 1
        return dp[1][-1]

# ============================================================================
# Solution 5: Bottom_Up_Space_Optimized    (原文件: 28 - 2787 - C - Ways to Express Integer Sum Power - Bottom Up Space Optimized 🚀🚀🚀.py)
# ============================================================================

n_5 = 4

x_5 = 1

class Solution_5_Bottom_Up_Space_Optimized:
    def numberOfWays(self, n_5: int, x_5: int) -> int:
        mod = 10**9 + 7

        dp = [0] * (n_5 + 1)
        root = math.ceil(n_5 ** (1 / x_5))
        val = root**x_5
        if 1 <= val <= n_5:
            dp[val] = 1

        for i in range(root - 1, 0, -1):
            new_dp = [0] * (n_5 + 1)
            pow = i**x_5
            for remain in range(1, n_5 + 1):
                if pow < remain:
                    new_dp[remain] = (dp[remain - pow] + dp[remain]) % mod
                elif pow == remain:
                    new_dp[remain] = 1
            dp = new_dp
        return dp[-1]


if __name__ == "__main__":

    # --- Solution 2: Top_Down_Memo ---
    s = Solution_2_Top_Down_Memo()
    result = s.numberOfWays(n_2, x_2)
    print(result)

    # --- Solution 4: Bottom_Up ---
    s = Solution_4_Bottom_Up()
    result = s.numberOfWays(n_4, x_4)
    print(result)

    # --- Solution 5: Bottom_Up_Space_Optimized ---
    s = Solution_5_Bottom_Up_Space_Optimized()
    result = s.numberOfWays(n_5, x_5)
    print(result)
