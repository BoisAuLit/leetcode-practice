"""LC-1920 - Build Array from Permutation

合并自 2 个解法文件:
  1. 007 - 1920 - A - Build Array From Permutation - (Bit Operation).py
  2. 007 - 1920 - B - Build Array From Permutation - (Bit Operation 👍).py
"""

from typing import List


# ============================================================================
# Solution 1: A    (原文件: 007 - 1920 - A - Build Array From Permutation - (Bit Operation).py)
# ============================================================================

# Time complexity: O()
# Space complexity: O()

nums_1 = [0,2,1,5,3,4] # Expecting [0,1,2,4,5,3]

# Runtime
# - 143ms
# - Beats 9.45%
#
# Memory
# - 16.65mb
# - Beats 28.44%

class Solution_1_A:
    def buildArray(self, nums_1: List[int]) -> List[int]:
        width = (999).bit_length()
        mask = (1 << width) - 1
        for i in range(len(nums_1)):
            nums_1[i] = nums_1[i] << width
        for i in range(len(nums_1)):
            nums_1[i] = nums_1[i] + (nums_1[nums_1[i] >> width] >> width)
        for i in range(len(nums_1)):
            nums_1[i] = nums_1[i] & mask
        return nums_1

# ============================================================================
# Solution 2: B    (原文件: 007 - 1920 - B - Build Array From Permutation - (Bit Operation 👍).py)
# ============================================================================

# Time complexity: O()
# Space complexity: O()

nums_2 = [0,2,1,5,3,4] # Expecting [0,1,2,4,5,3]

# Runtime
# - 127ms
# - Beats 84.08%
#
# Memory
# - 16.67mb
# - Beats 28.29%

class Solution_2_B:
    def buildArray(self, nums_2: List[int]) -> List[int]:
        bit_length = (999).bit_length()
        mask = (1 << bit_length) - 1
        for i, v in enumerate(nums_2):
            nums_2[i] += (nums_2[v] & mask) << bit_length
        for i in range(len(nums_2)):
            nums_2[i] >>= bit_length
        return nums_2


if __name__ == "__main__":

    # --- Solution 1: A ---
    s = Solution_1_A()
    result = s.buildArray(nums_1)
    print(result)

    # --- Solution 2: B ---
    s = Solution_2_B()
    result = s.buildArray(nums_2)
    print(result)
