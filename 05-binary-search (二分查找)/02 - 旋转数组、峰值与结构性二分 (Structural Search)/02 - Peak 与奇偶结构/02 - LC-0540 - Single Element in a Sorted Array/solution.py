"""LC-0540 - Single Element in a Sorted Array

合并自 2 个解法文件:
  1. 03 - 0540 - A - Single Elem In Sorted Array.py
  2. 03 - 0744 - A - Find smallest letter bigger than - Template 1.py
"""

from typing import List


# ============================================================================
# Solution 1: Single_Elem_In_Sorted_Array    (原文件: 03 - 0540 - A - Single Elem In Sorted Array.py)
# ============================================================================

class Solution_1_Single_Elem_In_Sorted_Array:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        lo = 0
        hi = len(nums) - 1
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if mid % 2 == 1:
                mid -= 1
            if nums[mid] == nums[mid + 1]:
                lo = mid + 2
            else:
                hi = mid
        return nums[lo]

# ============================================================================
# Solution 2: Template_1    (原文件: 03 - 0744 - A - Find smallest letter bigger than - Template 1.py)
# ============================================================================

letters = ["c", "f", "j"]

target = "a"

class Solution_2_Template_1:
    def nextGreatestLetter(self, letters: List[str], target: str) -> str:
        left = 0
        right = len(letters) - 1

        while left <= right:
            mid = (left + right) // 2
            if letters[mid] <= target: # 这一步非常关键
                left = mid + 1
            else:
                right = mid - 1

        if left == len(letters):
            return letters[0]
        else:
            return letters[left]


if __name__ == "__main__":

    # --- Solution 2: Template_1 ---
    s = Solution_2_Template_1()
    result = s.nextGreatestLetter(letters, target)
    print(result)
