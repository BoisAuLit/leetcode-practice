"""LC-0010 - Regular Expression Matching

合并自 3 个解法文件:
  1. 0010 - A(2) - Regex Matching - TLE ❌.py
  2. 0010 - B(2) - Regex Matching - DP - Top Down ⬇️.py
  3. 0010 - C(2) - Regex Matching - DP - Bottom Up ⬆️.py
"""


# ============================================================================
# Solution 1: TLE    (原文件: 0010 - A(2) - Regex Matching - TLE ❌.py)
# ============================================================================

text_1 = "aaabaaa"

pattern_1 = "a*b*a*"

class Solution_1_TLE(object):
    def isMatch(self, text_1: str, pattern_1: str) -> bool:
        if not pattern_1:
            return not text_1

        first_match = bool(text_1) and pattern_1[0] in {text_1[0], "."}

        if len(pattern_1) >= 2 and pattern_1[1] == "*":
            return (
                self.isMatch(text_1, pattern_1[2:])
                or first_match
                and self.isMatch(text_1[1:], pattern_1)
            )
        else:
            return first_match and self.isMatch(text_1[1:], pattern_1[1:])

# ============================================================================
# Solution 2: Top_Down    (原文件: 0010 - B(2) - Regex Matching - DP - Top Down ⬇️.py)
# ============================================================================

text_2 = "aaabaaa"

pattern_2 = "a*b*a*"

class Solution_2_Top_Down(object):
    def isMatch(self, text_2: str, pattern_2: str) -> bool:
        memo = {}

        def dp(i: int, j: int) -> bool:
            if (i, j) not in memo:
                if j == len(pattern_2):
                    ans = i == len(text_2)
                else:
                    first_match = i < len(text_2) and pattern_2[j] in {text_2[i], "."}
                    if j + 1 < len(pattern_2) and pattern_2[j + 1] == "*":
                        ans = dp(i, j + 2) or first_match and dp(i + 1, j)
                    else:
                        ans = first_match and dp(i + 1, j + 1)

                memo[i, j] = ans
            return memo[i, j]

        return dp(0, 0)

# ============================================================================
# Solution 3: Bottom_Up    (原文件: 0010 - C(2) - Regex Matching - DP - Bottom Up ⬆️.py)
# ============================================================================

text_3 = "aaabaaa"

pattern_3 = "a*b*a*"

class Solution_3_Bottom_Up(object):
    def isMatch(self, text_3: str, pattern_3: str) -> bool:
        memo = {}

        def dp(i: int, j: int) -> bool:
            if (i, j) not in memo:
                if j == len(pattern_3):
                    ans = i == len(text_3)
                else:
                    first_match = i < len(text_3) and pattern_3[j] in {text_3[i], "."}
                    if j + 1 < len(pattern_3) and pattern_3[j + 1] == "*":
                        ans = dp(i, j + 2) or first_match and dp(i + 1, j)
                    else:
                        ans = first_match and dp(i + 1, j + 1)

                memo[i, j] = ans
            return memo[i, j]

        return dp(0, 0)


if __name__ == "__main__":

    # --- Solution 1: TLE ---
    s = Solution_1_TLE()
    result = s.isMatch(text_1, pattern_1)
    print(result)

    # --- Solution 2: Top_Down ---
    s = Solution_2_Top_Down()
    result = s.isMatch(text_2, pattern_2)
    print(result)

    # --- Solution 3: Bottom_Up ---
    s = Solution_3_Bottom_Up()
    result = s.isMatch(text_3, pattern_3)
    print(result)
