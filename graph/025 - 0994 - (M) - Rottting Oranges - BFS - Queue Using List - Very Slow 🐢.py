from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        fresh = 0
        level = []
        for x in range(m):
            for y in range(n):
                if grid[x][y] == 1:
                    fresh += 1
                elif grid[x][y] == 2:
                    level.append((x, y))
                    grid[x][y] = 0
        if len(level) == 0 and fresh > 0:
            return -1
        if fresh == 0:
            return 0

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        minutes = 1
        while level:
            next_level = []
            for x, y in level:
                for dx, dy in directions:
                    x1, y1 = x + dx, y + dy
                    coords = (x1, y1)
                    if (
                        0 <= x1 <= m - 1
                        and 0 <= y1 <= n - 1
                        and grid[x1][y1] == 1
                    ):
                        grid[x1][y1] = 0
                        next_level.append(coords)
                        fresh -= 1
                        if fresh == 0:
                            return minutes
                level = next_level
            minutes += 1
        return -1


s = Solution()


# Test case 1: Expecting 4
grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
result = s.orangesRotting(grid)


print(result)
