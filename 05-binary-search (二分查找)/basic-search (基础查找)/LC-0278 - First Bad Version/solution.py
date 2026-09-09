"""LC-0278 - First Bad Version

合并自 3 个解法文件:
  1. 13 - 0278 - (1) - First Bad Version.py
  2. 02 - 0278 - A - First Bad Version - Template 1.py
  3. 02 - 0278 - B - First Bad Version - Template 2.py
"""


# ============================================================================
# Solution 1: First_Bad_Version    (原文件: 13 - 0278 - (1) - First Bad Version.py)
# ============================================================================

# Time complexity: O(logn)
# Space complexity: O(1)

input_ = 2

# Runtime
# - 45 ms
# - Beats 61.78%
#
# Memory
# - 16.2 MB
# - Beats 96.19%

def isBadVersion_1(n: int) -> bool:
    return n >= 2

class Solution_1_First_Bad_Version:
    def firstBadVersion(self, n: int) -> int:
        left = 1
        right = n

        while left <= right:
            mid = (left + right) // 2
            if isBadVersion_1(mid):
                if mid - 1 < 1:
                    return 1
                if not isBadVersion_1(mid - 1):
                    return mid
                right = mid
            else:
                left = mid + 1

# ============================================================================
# Solution 2: Template_1    (原文件: 02 - 0278 - A - First Bad Version - Template 1.py)
# ============================================================================

def isBadVersion_2(version: int) -> bool:
    return version >= 352

class Solution_2_Template_1:
    def firstBadVersion(self, n: int) -> int:
        left = 1
        right = n
        while left <= right:
            mid = (left + right) // 2

            if isBadVersion_2(mid):
                if not isBadVersion_2(mid - 1):
                    return mid
                else:
                    right = mid - 1
            else:
                left = mid + 1

# ============================================================================
# Solution 3: Template_2    (原文件: 02 - 0278 - B - First Bad Version - Template 2.py)
# ============================================================================

def isBadVersion_3(version: int) -> bool:
    return version >= 352

class Solution_3_Template_2:
    def firstBadVersion(self, n: int) -> int:
        left = 1
        right = n
        while left < right:
            mid = (left + right) // 2
            if isBadVersion_3(mid):
                if isBadVersion_3(mid - 1):
                    right = mid
                else:
                    return mid
            else:
                left = mid + 1
        return left


if __name__ == "__main__":

    # --- Solution 1: First_Bad_Version ---
    s = Solution_1_First_Bad_Version()
    result = s.firstBadVersion(input_)
    print(result)

    # --- Solution 2: Template_1 ---
    versions = range(1, 11)
    s = Solution_2_Template_1()
    result = s.firstBadVersion(687)
    print(result)

    # --- Solution 3: Template_2 ---
    versions = range(1, 11)
    s = Solution_3_Template_2()
    result = s.firstBadVersion(687)
    print(result)
