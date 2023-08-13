from typing import List

"""
Time complexity: O(mlog(n))
Space complexity: O(1)
"""


class Solution:
    def lastPositiveIndex(self, array: List[int]) -> int:
        if array[-1] >= 0:
            return len(array) - 1
        if array[0] < 0:
            return -1
        left = 0
        right = len(array) - 1
        while left < right:
            mid = (left + right) // 2
            if left == mid:
                return left
            if array[mid] >= 0:
                left = mid
            else:
                right = mid

    def countNegatives(self, grid: List[List[int]]) -> int:
        count = 0
        for array in grid:
            count += len(array) - 1 - self.lastPositiveIndex(array)
        return count


s = Solution()
grid = [
    [4, 3, 2, -1],
    [3, 2, 1, -1],
    [1, 1, -1, -2],
    [-1, -1, -2, -3],
]  # Expecting 6
result = s.countNegatives(grid)
print(result)
"""
Runtime
- 115ms
- Beats 90.69%

Memory
17.45mb
- Beats 67.37%
"""
