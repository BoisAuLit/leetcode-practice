"""LC-2768 - Number of Black Blocks

合并自 2 个解法文件:
  1. 001 - 2768 - A - Number of Black Blocks.py
  2. 001 - 3197 - A - Find Min Area Cover All Ones II.py
"""

from typing import List

from collections import defaultdict

import sys


# ============================================================================
# Solution 1: Number_of_Black_Blocks    (原文件: 001 - 2768 - A - Number of Black Blocks.py)
# ============================================================================

# Complexity Analysis:
#     - Time Complexity: O(n)
#     - Space Complexity: O(n)

class Solution_1_Number_of_Black_Blocks:
    def countBlackBlocks(self, m: int, n: int, coordinates: List[List[int]]) -> List[int]:
        block_counts = defaultdict(int)
        for x, y in coordinates:
            for dx, dy in [(-1,-1), (-1,0), (0,-1), (0,0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m - 1 and 0 <= ny < n - 1:
                    block_counts[(nx, ny)] += 1
        arr = [0] * 5
        for count in block_counts.values():
            arr[count] += 1
        total_blocks = (m - 1) * (n - 1)
        arr[0] = total_blocks - sum(arr[1:])
        return arr

# ============================================================================
# Solution 2: Find_Min_Area_Cover_All_Ones_II    (原文件: 001 - 3197 - A - Find Min Area Cover All Ones II.py)
# ============================================================================

class Solution_2_Find_Min_Area_Cover_All_Ones_II:
    def minimumSum2(
        self, grid: List[List[int]], u: int, d: int, l: int, r: int
    ) -> int:
        min_i = len(grid)
        max_i = 0
        min_j = len(grid[0])
        max_j = 0

        for i in range(u, d + 1):
            for j in range(l, r + 1):
                if grid[i][j] == 1:
                    min_i = min(min_i, i)
                    min_j = min(min_j, j)
                    max_i = max(max_i, i)
                    max_j = max(max_j, j)

        return (
            (max_i - min_i + 1) * (max_j - min_j + 1)
            if min_i <= max_i
            else sys.maxsize // 3
        )

    def rotate(self, vec: List[List[int]]) -> List[List[int]]:
        n = len(vec)
        m = len(vec[0]) if n > 0 else 0
        ret = [[0] * n for _ in range(m)]

        for i in range(n):
            for j in range(m):
                ret[m - j - 1][i] = vec[i][j]

        return ret

    def solve(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0]) if n > 0 else 0
        res = n * m

        for i in range(n - 1):
            for j in range(m - 1):
                res = min(
                    res,
                    self.minimumSum2(grid, 0, i, 0, m - 1)
                    + self.minimumSum2(grid, i + 1, n - 1, 0, j)
                    + self.minimumSum2(grid, i + 1, n - 1, j + 1, m - 1),
                )

                res = min(
                    res,
                    self.minimumSum2(grid, 0, i, 0, j)
                    + self.minimumSum2(grid, 0, i, j + 1, m - 1)
                    + self.minimumSum2(grid, i + 1, n - 1, 0, m - 1),
                )

        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                res = min(
                    res,
                    self.minimumSum2(grid, 0, i, 0, m - 1)
                    + self.minimumSum2(grid, i + 1, j, 0, m - 1)
                    + self.minimumSum2(grid, j + 1, n - 1, 0, m - 1),
                )

        return res

    def minimumSum(self, grid: List[List[int]]) -> int:
        rgrid = self.rotate(grid)
        return min(self.solve(grid), self.solve(rgrid))
