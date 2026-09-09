"""LC-1470 - Shuffle the Array

合并自 2 个解法文件:
  1. 006 - 1470 - A - Shuffle The Array - (Brute Force).py
  2. 006 - 1470 - B - Shuffle The Array - (In Place - bitwise ⭐️).py
"""

from typing import List


# ============================================================================
# Solution 1: Brute_Force    (原文件: 006 - 1470 - A - Shuffle The Array - (Brute Force).py)
# ============================================================================

# Time complexity: O(n_1)
# Space complexity: O(1)

nums_1 = [2, 5, 1, 3, 4, 7]

n_1 = 3  # Expecting [2, 3, 5, 4, 1, 7]

# Runtime
# - 77 ms
# - Beats 44.65%
#
# Memory
# - 16.5 MB
# - Beats 31.69%

class Solution_1_Brute_Force:
    def shuffle(self, nums_1: List[int], n_1: int) -> List[int]:
        result = [None] * (2 * n_1)
        result[0] = nums_1[0]
        result[-1] = nums_1[-1]
        for i in range(n_1 - 1, -1, -1):
            result[2 * i] = nums_1[i]
        for i in range(n_1 - 1):
            result[2 * i + 1] = nums_1[n_1 + i]
        return result

# ============================================================================
# Solution 2: bitwise    (原文件: 006 - 1470 - B - Shuffle The Array - (In Place - bitwise ⭐️).py)
# ============================================================================

# Time complexity: O(n_2)
# Space complexity: O(1)

nums_2 = [2, 5, 1, 3, 4, 7]

n_2 = 3  # Expecting [2, 3, 5, 4, 1, 7]

# Runtime
# - 72 ms
# - Beats 73.39%
#
# Memory
# - 16.5 MB
# - Beats 31.97%

class Solution_2_bitwise:
    def shuffle(self, nums_2: List[int], n_2: int) -> List[int]:
        last_ten_bits_mask = (1 << 10) - 1
        for i in range(n_2):
            nums_2[i] = (nums_2[i] << 10) + nums_2[i + n_2]
        for i in range(n_2 - 1, -1, -1):
            nums_2[2 * i + 1] = nums_2[i] & last_ten_bits_mask
            nums_2[2 * i] = nums_2[i] >> 10
        return nums_2


if __name__ == "__main__":

    # --- Solution 1: Brute_Force ---
    s = Solution_1_Brute_Force()
    result = s.shuffle(nums_1, n_1)
    print(result)

    # --- Solution 2: bitwise ---
    s = Solution_2_bitwise()
    result = s.shuffle(nums_2, n_2)
    print(result)
