"""LC-0200 - Number of Islands

阶段 1 · DFS、BFS（静态无权的连通性与步数）· 洪水填充（数连通块）★ 签名题
题目在问：静态网格里有几个岛（上下左右相连的 "1" 算同一个岛）
点是什么：一个格子   边是什么：上下左右四邻居里的 "1"
和签名题比改了哪一行：本题就是 DFS 洪水填充签名题
"""
from typing import List
from collections import deque


##################################################################################################
##### ! Solution 1: 递归 DFS 洪水填充
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)（递归栈最坏时是整座岛）
##### ! 适用：静态网格数连通块的默认写法，最短最常考；m·n ≤ 9e4，LeetCode 的递归上限够用，本地大图要 sys.setrecursionlimit
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


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


##################################################################################################
##### ! Solution 2: 迭代 DFS（显式栈）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：和 Solution 1 等价、不怕爆栈；这里出栈时才标记，同一格最多入栈 4 次，仍是 O(m·n)
##################################################################################################


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


##################################################################################################
##### ! Solution 3: BFS 洪水填充
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：入队时立即标记，每格只进队一次；要顺便求步数/层数时换成它
##################################################################################################


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


##################################################################################################
##### ! Solution 4: 并查集
##### ! 时间复杂度: O(m·n·α(m·n))   空间复杂度: O(m·n)
##### ! 适用：静态网格用它是杀鸡用牛刀，只为对照；真正需要它的是动态加陆地的 LC-0305
##################################################################################################


class UnionFind:  # 路径减半 + 按 size 合并，union 返回是否真的合并了（和 LC-1135 里的一样）
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


class Solution_4:
    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])
        uf = UnionFind(m * n)  # 格子 (x, y) 编号为 x * n + y
        count = sum(row.count("1") for row in grid)  # ! 先把每个 "1" 都当成一座岛
        for x in range(m):
            for y in range(n):
                if grid[x][y] != "1":
                    continue
                for nx, ny in ((x + 1, y), (x, y + 1)):  # ! 只看右、下，每条边只合并一次
                    if nx < m and ny < n and grid[nx][ny] == "1" and uf.union(x * n + y, nx * n + ny):
                        count -= 1  # ! 每次真的合并，岛就少一座
        return count


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
