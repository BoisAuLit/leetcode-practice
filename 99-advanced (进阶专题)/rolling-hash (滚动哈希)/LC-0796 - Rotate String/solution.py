"""LC-0796 - Rotate String

合并自 2 个解法文件:
  1. 0796-A - Rotate String.py
  2. 0796-B - Rotate String - (👍 Rolling Hash).py
"""

from typing import List


# ============================================================================
# Solution 1: Rotate_String    (原文件: 0796-A - Rotate String.py)
# ============================================================================

# Time complexity: O(N²)
# Space complexity: O(N)

class Solution_1_Rotate_String:
    def rotateString(self, s: str, goal: str) -> bool:
        return len(s) == len(goal) and goal in s * 2

# ============================================================================
# Solution 2: Rolling_Hash    (原文件: 0796-B - Rotate String - (👍 Rolling Hash).py)
# ============================================================================

class Solution_2_Rolling_Hash(object):
    def rotateString(self, A, B):
        MOD = 10**9 + 7
        P = 113
        Pinv = pow(P, MOD - 2, MOD)

        hb = 0
        power = 1
        for x in B:
            code = ord(x) - 96
            hb = (hb + power * code) % MOD
            power = power * P % MOD

        ha = 0
        power = 1
        for x in A:
            code = ord(x) - 96
            ha = (ha + power * code) % MOD
            power = power * P % MOD

        if ha == hb and A == B:
            return True
        for i, x in enumerate(A):
            code = ord(x) - 96
            ha += power * code
            ha -= code
            ha *= Pinv
            ha %= MOD
            if ha == hb and A[i + 1 :] + A[: i + 1] == B:
                return True
        return False
