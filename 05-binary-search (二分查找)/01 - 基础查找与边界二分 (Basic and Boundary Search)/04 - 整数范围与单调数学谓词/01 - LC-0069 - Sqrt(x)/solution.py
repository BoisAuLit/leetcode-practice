"""LC-0069 - Sqrt(x)

合并自 2 个解法文件:
  1. 11 - 0069 - (1) - Sqrt(x).py
  2. 02 - 0069 - A - Sqrt(x).py
"""


# ============================================================================
# Solution 1: V1    (原文件: 11 - 0069 - (1) - Sqrt(x).py)
# ============================================================================

# Time complexity: O(logn)
# Space complexity: O(1)

input_ = 4

# Runtime
# - 54 ms
# - Beats 53.32%
#
# Memory
# - 16.4 MB
# - Beats 15.80%

class Solution_1_V1:
    def mySqrt(self, x):
        if x < 2:
            return x
        left = 1
        right = x
        while True:
            if right - left <= 1:
                return left
            pivot = (left + right) // 2
            pivot_square = pivot * pivot
            if pivot_square == x:
                return pivot
            if pivot_square < x:
                left = pivot
            else:
                right = pivot

# ============================================================================
# Solution 2: A    (原文件: 02 - 0069 - A - Sqrt(x).py)
# ============================================================================

class Solution_2_A:
    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x

        left = 2
        right = x // 2

        while left <= right:
            mid = (left + right) // 2
            num = mid * mid
            if num > x:
                right = mid - 1
            elif num < x:
                left = mid + 1
            else:
                return mid

        return right


if __name__ == "__main__":

    # --- Solution 1: V1 ---
    s = Solution_1_V1()
    result = s.mySqrt(input_)
    print(result)
