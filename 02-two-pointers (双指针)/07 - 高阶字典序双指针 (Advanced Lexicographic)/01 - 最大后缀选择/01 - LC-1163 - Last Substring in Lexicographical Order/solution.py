"""LC-1163 - Last Substring in Lexicographical Order

合并自 2 个解法文件:
  1. 001 - 1163 - A(1) - Last Substring in Lexi Order.py
  2. 001 - 1163 - B(1) - Last Substring in Lexi Order (1).py
"""


# ============================================================================
# Solution 1: Last_Substring_in_Lexi_Order    (原文件: 001 - 1163 - A(1) - Last Substring in Lexi Order.py)
# ============================================================================

class Solution_1_Last_Substring_in_Lexi_Order:
    def lastSubstring(self, s: str) -> str:
        i, j, k = 0, 1, 0
        n = len(s)
        while j + k < n:
            if s[i + k] == s[j + k]:
                k += 1
                continue
            elif s[i + k] > s[j + k]:
                j = j + k + 1
            else:
                i = max(i + k + 1, j)
                j = i + 1
            k = 0
        return s[i:]

# ============================================================================
# Solution 2: Last_Substring_in_Lexi_Order_1    (原文件: 001 - 1163 - B(1) - Last Substring in Lexi Order (1).py)
# ============================================================================

class Solution_2_Last_Substring_in_Lexi_Order_1:
    def lastSubstring(self, s: str) -> str:
        i, j, k = 0, 1, 0
        n = len(s)
        while j + k < n:
            if s[i + k] == s[j + k]:
                k += 1
                continue
            elif s[i + k] > s[j + k]:
                j = j + k + 1
            else:
                i = max(i + k + 1, j)
                j = i + 1
            k = 0
        return s[i:]
