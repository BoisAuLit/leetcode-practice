"""LC-1770 - Maximum Score from Performing Multiplication Operations

合并自 3 个解法文件:
  1. 06 - 1770 - A - Max Score Multiply - Top Down - Recursive - Memo -  🐢🐢🐢.py
  2. 06 - 1770 - B - Max Score Multiply - Bottom Up - 🚀.py
  3. 06 - 1770 - C - Max Score Multiply - Bottop Up - Space Optimized - 🚀🚀🚀.py
"""

from typing import List

from functools import cache


# ============================================================================
# Solution 1: Memo    (原文件: 06 - 1770 - A - Max Score Multiply - Top Down - Recursive - Memo -  🐢🐢🐢.py)
# ============================================================================

class Solution_1_Memo:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        @cache
        def dp(l: int, r: int) -> int:
            # ! l --> left pointer in nums
            # ! r --> right pointer in nums (not taking how many from right side)
            m = l + len(nums) - 1 - r
            if m >= len(multipliers):
                return 0

            return max(
                nums[l] * multipliers[m] + dp(l + 1, r),
                nums[r] * multipliers[m] + dp(l, r - 1),
            )

        return dp(0, len(nums) - 1)

# ============================================================================
# Solution 2: Bottom_Up    (原文件: 06 - 1770 - B - Max Score Multiply - Bottom Up - 🚀.py)
# ============================================================================

class Solution_2_Bottom_Up:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        n = len(nums)
        m = len(multipliers)
        dp = [[0] * (m + 1) for _ in range(m + 1)]
        max_ = float("-inf")
        for i in range(1, m + 1):
            dp[0][i] = dp[0][i - 1] + nums[n - i] * multipliers[i - 1]
            dp[i][0] = dp[i - 1][0] + nums[i - 1] * multipliers[i - 1]
            if i == m:
                max_ = max(max_, dp[0][i], dp[i][0])

        for i in range(1, m + 1):
            for j in range(1, m + 1 - i):
                k = i + j - 1
                dp[i][j] = max(
                    # Take one from left
                    dp[i - 1][j] + multipliers[k] * nums[i - 1],
                    # Take one from right
                    dp[i][j - 1] + multipliers[k] * nums[n - j],
                )
                if i + j == m:
                    max_ = max(max_, dp[i][j])
        return max_

# ============================================================================
# Solution 3: Space_Optimized    (原文件: 06 - 1770 - C - Max Score Multiply - Bottop Up - Space Optimized - 🚀🚀🚀.py)
# ============================================================================

class Solution_3_Space_Optimized:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        n = len(nums)
        m = len(multipliers)
        dp = [0] * (m + 1)
        # ! Initialize the first dp array
        for i in range(1, m + 1):
            dp[i] = dp[i - 1] + nums[n - i] * multipliers[i - 1]
        # ! Initialize the maximum value
        max_ = dp[-1]
        for i in range(1, m + 1):
            # ! dp[0] means only take numbers on left side
            dp[0] += nums[i - 1] * multipliers[i - 1]
            for j in range(1, m - i + 1):
                k = i + j - 1
                dp[j] = max(
                    nums[i - 1] * multipliers[k] + dp[j],  # Take from left
                    nums[n - j] * multipliers[k] + dp[j - 1],  # Take from right
                )
                if i + j == m:
                    max_ = max(max_, dp[j])
        return max_
