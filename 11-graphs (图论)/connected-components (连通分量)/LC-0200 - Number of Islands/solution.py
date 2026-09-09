from typing import List
from collections import deque


class Solution_DFS_Recursive:
    def numIslands(self, grid: List[List[str]]) -> int:

        res = 0
        m = len(grid)
        n = len(grid[0])

        def dfs(x, y):
            if not (0 <= x < m and 0 <= y < n) or grid[x][y] != "1":
                return
            grid[x][y] = "0"
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                dfs(nx, ny)

        for x in range(m):
            for y in range(n):
                if grid[x][y] == "1":
                    res += 1
                    dfs(x, y)

        return res


class Solution_DFS_Iterative_Stack:
    def numIslands(self, grid: List[List[str]]) -> int:

        res = 0
        m = len(grid)
        n = len(grid[0])

        def dfs(x, y):
            nonlocal m, n, grid
            stack = [(x, y)]
            while stack:
                x, y = stack.pop()
                grid[x][y] = "0"
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == "1":
                        stack.append((nx, ny))

        for x in range(m):
            for y in range(n):
                if grid[x][y] == "1":
                    res += 1
                    dfs(x, y)

        return res


class Solution_BFS:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0

        res = 0
        m = len(grid)
        n = len(grid[0])

        def bfs(start_x, start_y):
            q = deque([(start_x, start_y)])

            # 一进入队列就标记，防止被重复加入
            grid[start_x][start_y] = "0"

            while q:
                x, y = q.popleft()

                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == "1":
                        # 入队时立即标记
                        grid[nx][ny] = "0"
                        q.append((nx, ny))

        for x in range(m):
            for y in range(n):
                if grid[x][y] == "1":
                    res += 1
                    bfs(x, y)

        return res


s = Solution_BFS()
# fmt: off
input_ = [
    ["1","1","0","0","1"],
    ["1","1","0","0","1"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
  ]
# fmt: on
result = s.numIslands(input_)
print(result)
