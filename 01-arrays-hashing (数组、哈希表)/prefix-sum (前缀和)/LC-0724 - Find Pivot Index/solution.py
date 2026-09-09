"""LC-0724 - Find Pivot Index

合并自 2 个解法文件:
  1. 04 - 0724-A - Find Pivot Index.py
  2. 04 - 0724-B - Find Pivot Index 👍.py
"""

from typing import List


# ============================================================================
# Solution 1: V1    (原文件: 04 - 0724-A - Find Pivot Index.py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(1)

# Runtime
# - 171ms
# - Beats 36.46%
#
# Memory
# 17.72mb
# - Beats 7.81%

class Solution_1_V1:
    def pivotIndex(self, nums: List[int]) -> int:
        left_sum = 0
        right_sum = sum(nums[1:])
        for i in range(len(nums)):
            if left_sum == right_sum:
                return i
            if i == len(nums) - 1:
                break
            left_sum += nums[i]
            right_sum -= nums[i + 1]
        return -1

# ============================================================================
# Solution 2: V2    (原文件: 04 - 0724-B - Find Pivot Index 👍.py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(1)

# Runtime
# - 162ms
# - Beats 63.37%
#
# Memory
# 17.70mb
# - Beats 7.81%

class Solution_2_V2:
    def pivotIndex(self, nums: List[int]) -> int:
        sum_ = sum(nums)
        left_sum = 0
        for i in range(len(nums)):
            if left_sum == sum_ - nums[i] - left_sum:
                return i
            left_sum += nums[i]
        return -1
