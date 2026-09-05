from typing import List
from collections import deque


class Solution:
    def islandsAndTreasure(self, grid: List[List[int]]) -> None:
        m = len(grid)
        n = len(grid[0])

        INF = 2**31 - 1

        q = deque([(x, y) for x in range(m) for y in range(n) if grid[x][y] == 0])

        while q:
            x, y = q.popleft()

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == INF:
                    grid[nx][ny] = grid[x][y] + 1
                    q.append((nx, ny))


s = Solution()
input_ = [
    [2147483647, -1, 0, 2147483647],
    [2147483647, 2147483647, 2147483647, -1],
    [2147483647, -1, 2147483647, -1],
    [0, -1, 2147483647, 2147483647],
]
result = s.islandsAndTreasure(input_)
print(result)
