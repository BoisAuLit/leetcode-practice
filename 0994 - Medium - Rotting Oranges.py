from typing import List
from functools import lru_cache


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        fresh = 0
        level = []

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    fresh += 1
                elif grid[i][j] == 2:
                    level.append((i, j))

        if fresh == 0:
            return 0
        if len(level) == 0 and fresh > 0:
            return -1

        newly_rotton_count = 0
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        def in_grid(x: int, y: int) -> bool:
            return 0 <= x < m and 0 <= y < n

        minutes = 0
        iteration = 0
        while True:
            iteration += 1
            new_level = []
            minutes += 1
            for row, col in level:
                for x, y in directions:
                    x1, y1 = row + x, col + y
                    if in_grid(x1, y1) and grid[x1][y1] == 1:
                        newly_rotton_count += 1
                        new_level.append((x1, y1))
                        grid[x1][y1] = 2
            level = new_level
            if newly_rotton_count == fresh:
                return minutes
            if iteration > m * n:
                return -1


s = Solution()

# Test case 1: Expecting 4
input_ = [[2, 1, 1], [0, 1, 1], [1, 0, 1]]
# input_ = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
result = s.orangesRotting(input_)
print(result)
