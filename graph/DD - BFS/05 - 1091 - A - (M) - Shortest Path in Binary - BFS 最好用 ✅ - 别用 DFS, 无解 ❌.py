from typing import List
from collections import deque


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        if grid[0][0] + grid[-1][-1] != 0:
            return -1
        n = len(grid)
        directions = [
            (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy
        ]
        queue = deque([(0, 0, 1)])
        seen = {(0, 0)}
        while queue:
            x, y, d = queue.popleft()
            if (x, y) == (n - 1, n - 1):
                return d
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < n
                    and 0 <= ny < n
                    and grid[nx][ny] == 0
                    and (nx, ny) not in seen
                ):
                    seen.add((nx, ny))
                    queue.append((nx, ny, d + 1))
        return -1


# Case 1: Expect 4
s = Solution()
grid = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
result = s.shortestPathBinaryMatrix(grid)
print(result)
