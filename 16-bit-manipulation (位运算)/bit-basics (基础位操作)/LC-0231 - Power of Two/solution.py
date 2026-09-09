"""LC-0231 - Power of Two

合并自 4 个解法文件:
  1. 003 - 0231 - A - Power Of 2 - (Brute Force).py
  2. 003 - 0231 - B - Power Of 2 - (Bitwise).py
  3. 003 - 0231 - C - Power Of 2 - (Bitwise 👍).py
  4. 003 - 0231 - D - Power Of 2 - (Bitwise 👍).py
"""

from typing import List


# ============================================================================
# Solution 1: Brute_Force    (原文件: 003 - 0231 - A - Power Of 2 - (Brute Force).py)
# ============================================================================

# Time complexity: O(logn)
# Space complexity: O(logn)

input__1 = 16 #‚ Expecting True

# Runtime
# - 59ms
# - Beats 7.89%
#
# Memory
# - 16.24mb
# - Beats 65.84%

class Solution_1_Brute_Force:
    def isPowerOfTwo(self, n: int) -> bool:
        if n <= 0:
            return False
        return all(x == '0' for x in list(bin(n)[3:]))

# ============================================================================
# Solution 2: B    (原文件: 003 - 0231 - B - Power Of 2 - (Bitwise).py)
# ============================================================================

# Time complexity: O()
# Space complexity: O()

input__2 = 16 #‚ Expecting True

# Runtime
# - 43ms
# - Beats 85.24%
#
# Memory
# - 16.24mb
# - Beats 65.84%

class Solution_2_B:
    def isPowerOfTwo(self, n: int) -> bool:
        if n <= 0:
            return False
        nb_digits = len(bin(n)[2:])
        mask = (1 << (nb_digits)) - 1
        return ((n ^ mask) + 1) == n

# ============================================================================
# Solution 3: C    (原文件: 003 - 0231 - C - Power Of 2 - (Bitwise 👍).py)
# ============================================================================

# Time complexity: O(1)
# Space complexity: O(1)

input__3 = 16 #‚ Expecting True


class Solution_3_C(object):
    def isPowerOfTwo(self, n):
        if n == 0:
            return False
        return n & (-n) == n

# ============================================================================
# Solution 4: D    (原文件: 003 - 0231 - D - Power Of 2 - (Bitwise 👍).py)
# ============================================================================

# Time complexity: O()
# Space complexity: O()

input__4 = 16 #‚ Expecting True


class Solution_4_D(object):
    def isPowerOfTwo(self, n):
        if n == 0:
            return False
        return n & (n - 1) == 0


if __name__ == "__main__":

    # --- Solution 1: Brute_Force ---
    s = Solution_1_Brute_Force()
    result = s.isPowerOfTwo(input__1)
    print(result)

    # --- Solution 2: B ---
    s = Solution_2_B()
    result = s.isPowerOfTwo(input__2)
    print(result)

    # --- Solution 3: C ---
    s = Solution_3_C()
    result = s.isPowerOfTwo(input__3)
    print(result)

    # --- Solution 4: D ---
    s = Solution_4_D()
    result = s.isPowerOfTwo(input__4)
    print(result)
