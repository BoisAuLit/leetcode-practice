"""LC-0704 - Binary Search

合并自 3 个解法文件:
  1. 01 - 0704 - A - Binary Search - Template 1.py
  2. 01 - 0704 - A - Binary Search - Template 2.py
  3. 01 - 0704 - A - Binary Search - Template 3.py
"""

from typing import List


# ============================================================================
# Solution 1: Template_1    (原文件: 01 - 0704 - A - Binary Search - Template 1.py)
# ============================================================================

class Solution_1_Template_1:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            m = (left + right) // 2
            if nums[m] < target:
                left = m + 1
            elif nums[m] > target:
                right = m - 1
            else:
                return m
        return -1

# ============================================================================
# Solution 2: Template_2    (原文件: 01 - 0704 - A - Binary Search - Template 2.py)
# ============================================================================

class Solution_2_Template_2:
    def search(self, nums: List[int], target: int) -> int:
        if len(nums) == 0:
            return -1
        left = 0
        right = len(nums) - 1

        while left < right:
            mid = (left+right)//2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid+1
            else:
                right = mid
        if nums[left] == target:
            return left
        return -1

# ============================================================================
# Solution 3: Template_3    (原文件: 01 - 0704 - A - Binary Search - Template 3.py)
# ============================================================================

class Solution_3_Template_3:
    def search(self, nums: List[int], target: int) -> int:
        if len(nums) == 0:
            return -1

        left, right = 0, len(nums) - 1
        while left + 1 < right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid
            else:
                right = mid
        if nums[left] == target:
            return left
        if nums[right] == target:
            return right
        return -1
