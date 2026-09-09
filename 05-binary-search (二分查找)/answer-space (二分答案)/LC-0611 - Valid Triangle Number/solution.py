"""LC-0611 - Valid Triangle Number

合并自 2 个解法文件:
  1. 04 - 0611 - A - Valid Triangle Number - Binary Seaarch 🐢.py
  2. 04 - 0611 - B - Valid Triangle Number - Linear Scan 🚀.py
"""

from typing import List


# ============================================================================
# Solution 1: Binary_Seaarch    (原文件: 04 - 0611 - A - Valid Triangle Number - Binary Seaarch 🐢.py)
# ============================================================================

class Solution_1_Binary_Seaarch:
    def triangleNumber(self, nums: List[int]) -> int:
        n = len(nums)
        def binary_search(l: int, r: int, x: int) -> int:
            # Find the first index >= x in the range [l, r]
            while r >= l and r < n:
                mid = (l + r) // 2
                if nums[mid] >= x:
                    r = mid - 1
                else:
                    l = mid + 1
            return l

        nums.sort()
        res = 0

        for i in range(n - 2):
            k = i + 2
            for j in range(i + 1, n - 1):
                if nums[i] == 0:
                    break
                k = binary_search(k, n - 1, nums[i] + nums[j])
                res += k - j - 1

        return res

# ============================================================================
# Solution 2: Linear_Scan    (原文件: 04 - 0611 - B - Valid Triangle Number - Linear Scan 🚀.py)
# ============================================================================

class Solution_2_Linear_Scan:
    def triangleNumber(self, nums: List[int]) -> int:
        nums.sort()
        n = len(nums)
        count = 0

        for i in range(n - 2):
            if nums[i] == 0:
                continue   # 0 不能作为三角形最小边

            k = i + 2
            for j in range(i + 1, n - 1):
                # 线性推进 k，不回退
                while k < n and nums[i] + nums[j] > nums[k]:
                    k += 1

                # [j+1, k-1] 都可以作为第三条边
                count += k - j - 1

        return count
