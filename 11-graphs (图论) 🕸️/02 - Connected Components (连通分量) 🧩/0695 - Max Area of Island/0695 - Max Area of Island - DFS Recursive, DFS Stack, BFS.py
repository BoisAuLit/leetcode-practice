from typing import List
from collections import deque


class Solution_DFS_Recursive:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        res = 0
        m = len(grid)
        n = len(grid[0])

        def dfs(x, y):
            if not (0 <= x < m and 0 <= y < n) or grid[x][y] == 0:
                return 0
            grid[x][y] = 0
            return 1 + sum(dfs(x + dx, y + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)])

        for x in range(m):
            for y in range(n):
                res = max(res, dfs(x, y))
        return res


class Solution_DFS_Iterative_Stack:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0

        res = 0
        m = len(grid)
        n = len(grid[0])

        def dfs(x, y):
            stack = [(x, y)]
            grid[x][y] = 0  # 入栈时立即标记
            area = 0

            while stack:
                x, y = stack.pop()
                area += 1

                for dx, dy in [
                    (0, 1),
                    (0, -1),
                    (1, 0),
                    (-1, 0),
                ]:
                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                        grid[nx][ny] = 0  # 先标记
                        stack.append((nx, ny))

            return area

        for x in range(m):
            for y in range(n):
                if grid[x][y] == 1:
                    res = max(res, dfs(x, y))

        return res


class Solution_BFS_Queue:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        maxArea = 0
        m = len(grid)
        n = len(grid[0])

        def dfs(x, y):
            nonlocal maxArea
            currArea = 1
            grid[x][y] = 0
            q = deque([(x, y)])
            while q:
                x, y = q.popleft()
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                        currArea += 1
                        grid[nx][ny] = 0
                        q.append((nx, ny))
            maxArea = max(maxArea, currArea)

        for x in range(m):
            for y in range(n):
                if grid[x][y] == 1:
                    dfs(x, y)
        return maxArea


s = Solution_DFS_Iterative_Stack()
# fmt: off
grid = [
  [0,1,1,0,1],
  [1,0,1,0,1],
  [0,1,1,0,1],
  [0,1,0,0,1]
]
# fmt: on
result = s.maxAreaOfIsland(grid)
print(result)
