from typing import List
from collections import deque


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        fresh = 0
        queue = deque()

        for x in range(m):
            for y in range(n):
                if grid[x][y] == 1:
                    fresh += 1
                elif grid[x][y] == 2:
                    queue.append((x, y))

        if fresh == 0:
            return 0
        if not queue:
            return -1

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        minutes = 0

        while queue:
            minutes += 1
            for _ in range(len(queue)):
                x, y = queue.popleft()
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                        grid[nx][ny] = 2
                        queue.append((nx, ny))
                        fresh -= 1
                        if fresh == 0:
                            return minutes

        return -1


s = Solution()


# Test case 1: Expecting 4
grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
result = s.orangesRotting(grid)


print(result)
