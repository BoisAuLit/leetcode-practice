"""LC-0695 - Max Area of Island

阶段 1 · DFS、BFS（静态无权的连通性与步数）· 洪水填充（数连通块）○ 核心
题目在问：最大的岛有几格
点是什么：一个格子   边是什么：上下左右四邻居里的 1
和签名题比改了哪一行：和 200 比，dfs 不再只是淹掉，而是返回 1 + 四个方向的面积之和，外层取 max
"""
from typing import List
from collections import deque


##################################################################################################
##### ! Solution 1: 递归 DFS 返回面积
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)（递归栈最坏时是整座岛）
##### ! 适用：200 改一行就是它；外层不用先判 1，dfs 对 0 格直接返回 0
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


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


##################################################################################################
##### ! Solution 2: 迭代 DFS（显式栈）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：入栈时立即标记，每格只入栈一次，出栈时 area += 1；怕爆栈时用
##################################################################################################


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


##################################################################################################
##### ! Solution 3: BFS
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：和 Solution 2 只差 pop 换 popleft；这题不要层数，队列和栈等价
##################################################################################################


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
