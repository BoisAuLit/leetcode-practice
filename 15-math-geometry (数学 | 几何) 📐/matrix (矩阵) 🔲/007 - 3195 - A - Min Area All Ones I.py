from typing import List


class Solution:
    def minimumArea(self, grid: List[List[int]]) -> int:
        top = 1000
        right = -1
        left = 1000
        bottom = -1
        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    continue
                top = min(top, i)
                bottom = max(bottom, i)
                left = min(left, j)
                right = max(right, j)
        height = bottom - top + 1
        width = right - left + 1
        return width * height
