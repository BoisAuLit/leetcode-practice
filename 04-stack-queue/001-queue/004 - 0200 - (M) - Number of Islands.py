from typing import List
from collections import deque


# ! Method 1
class Solution:
    def bfs(self, x: int, y: int, grid: List[List[int]]) -> None:
        grid[x][y] = "0"
        queue = deque([(x, y)])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        m = len(grid)
        n = len(grid[0])
        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                x1, y1 = x + dx, y + dy
                if 0 <= x1 < m and 0 <= y1 < n and grid[x1][y1] == "1":
                    grid[x1][y1] = "0"
                    queue.append((x1, y1))

    def numIslands(self, grid: List[List[str]]) -> int:
        m = len(grid)
        n = len(grid[0])
        count = 0
        for x in range(m):
            for y in range(n):
                if grid[x][y] == "1":
                    count += 1
                    self.bfs(x, y, grid)
        return count


s = Solution()

# fmt: off
# Test case 1: expecting 1
grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]

# Test case 2: Expecting 3
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]

# fmt: on

result = s.numIslands(grid)
print(result)
