"""LC-0034 - Find First and Last Position of Element in Sorted Array

合并自 2 个解法文件:
  1. 09 - 0034 - (1) - 1st and last position.py
  2. 02 - 0034 - A - Find 1st & last position sorted array.py
"""

from typing import List

from bisect import bisect_left, bisect_right


# ============================================================================
# Solution 1: V1    (原文件: 09 - 0034 - (1) - 1st and last position.py)
# ============================================================================

# Time complexity: O(logn)
# Space complexity: O(1)

nums = [2, 2]

target_1 = 3

class Solution_1_V1:
    def searchRange(self, nums: List[int], target_1: int) -> List[int]:
        
        def binary_search(nums, target_1, is_searching_left):
            left = 0
            right = len(nums) - 1
            idx = -1
            
            while left <= right:
                mid = (left + right) // 2
                
                if nums[mid] > target_1:
                    right = mid - 1
                elif nums[mid] < target_1:
                    left = mid + 1
                else:
                    idx = mid
                    if is_searching_left:
                        right = mid - 1
                    else:
                        left = mid + 1
            
            return idx
        
        left = binary_search(nums, target_1, True)
        right = binary_search(nums, target_1, False)
        
        return [left, right]

# ============================================================================
# Solution 2: Find_1st_last_position_sorted_array    (原文件: 02 - 0034 - A - Find 1st & last position sorted array.py)
# ============================================================================

input_ = [2, 2]

target_2 = 3

class Solution_2_Find_1st_last_position_sorted_array:
    def searchRange(self, nums: List[int], target_2: int) -> List[int]:
        n = len(nums)
        if n == 0:
            return [-1, -1]
        lower = bisect_left(nums, target_2)

        if not 0 <= lower <= n - 1 or nums[lower] != target_2:
            return [-1, -1]

        upper = bisect_right(nums, target_2)

        return [lower, upper - 1]


if __name__ == "__main__":

    # --- Solution 1: V1 ---
    s = Solution_1_V1()
    result = s.searchRange(nums, target_1)
    print(result)

    # --- Solution 2: Find_1st_last_position_sorted_array ---
    s = Solution_2_Find_1st_last_position_sorted_array()
    result = s.searchRange(input_, target_2)
    print(result)
