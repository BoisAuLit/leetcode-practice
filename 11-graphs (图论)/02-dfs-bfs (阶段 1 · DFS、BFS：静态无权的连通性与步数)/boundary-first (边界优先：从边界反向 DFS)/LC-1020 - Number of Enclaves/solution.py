"""LC-1020 - Number of Enclaves

阶段 1 · 边界优先(从边界反向 DFS) ○ 核心变体
题目在问：1 是陆地 0 是海，有多少个陆地格无论怎么走都走不出网格边界
点是什么：一个格子   边是什么：上下左右相邻且同为 1
和签名题比改了哪一行：和 1254 同一个套路，先从四条边上的 1 出发把"能走出去"的陆地全淹掉，
    剩下的 1 的个数就是答案。区别：1254 数岛(连通块个数)，本题数格子(剩余 1 的个数)。
    网格到 500x500 = 2.5e5 格，递归会爆栈，所以这里全用显式栈 / 队列 / 并查集，没写递归版。
"""
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

##################################################################################################
##### ! Solution 1: 边界优先 DFS(显式栈)淹掉，再数剩下的 1
##### ! 时间复杂度: O(m · n)   空间复杂度: O(m · n)  (栈)
##### ! 适用：1254 同款两步走；显式栈是因为 2.5e5 格递归会爆
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numEnclaves(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        def flood(sr: int, sc: int) -> None:
            if grid[sr][sc] != 1:
                return
            grid[sr][sc] = 0  # ! 淹掉：陆地改成海，兼当 visited
            stack = [(sr, sc)]
            while stack:
                r, c = stack.pop()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                        grid[nr][nc] = 0
                        stack.append((nr, nc))

        # ! 第一步：边界优先，四条边上的 1 出发，能连到边界的陆地全淹掉
        for r in range(m):
            flood(r, 0)
            flood(r, n - 1)
        for c in range(n):
            flood(0, c)
            flood(m - 1, c)

        # ! 第二步：剩下的 1 都走不出去，数格子(不是数岛)
        return sum(row.count(1) for row in grid)


##################################################################################################
##### ! Solution 2: 多源 BFS，四条边上的 1 一起入队
##### ! 时间复杂度: O(m · n)   空间复杂度: O(m · n)  (队列)
##### ! 适用：994 的多源写法搬过来；一次 BFS 代替四条边各 flood 一次
##################################################################################################


class Solution_2:
    def numEnclaves(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        queue = deque()
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1 and (r == 0 or r == m - 1 or c == 0 or c == n - 1):
                    grid[r][c] = 0
                    queue.append((r, c))  # ! 多源：所有边界陆地一起当起点

        while queue:
            r, c = queue.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 0
                    queue.append((nr, nc))

        return sum(row.count(1) for row in grid)


##################################################################################################
##### ! Solution 3: 并查集 + 虚拟"边界点"
##### ! 时间复杂度: O(m · n · α)   空间复杂度: O(m · n)
##### ! 适用：不改 grid、不用遍历时的另一条路；边界上的 1 和虚拟点合并，最后数根不是虚拟点的 1
##################################################################################################


class UnionFind:
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


class Solution_3:
    def numEnclaves(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        border = m * n  # ! 多开一格当虚拟边界点
        uf = UnionFind(m * n + 1)
        for r in range(m):
            for c in range(n):
                if grid[r][c] != 1:
                    continue
                idx = r * n + c
                if r == 0 or r == m - 1 or c == 0 or c == n - 1:
                    uf.union(idx, border)  # ! 边界陆地直接挂到虚拟点上
                if r + 1 < m and grid[r + 1][c] == 1:
                    uf.union(idx, idx + n)
                if c + 1 < n and grid[r][c + 1] == 1:
                    uf.union(idx, idx + 1)  # 只看右、下，每条边只合并一次

        root_border = uf.find(border)
        return sum(
            1
            for r in range(m)
            for c in range(n)
            if grid[r][c] == 1 and uf.find(r * n + c) != root_border
        )


s = Solution_1()
grid = [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
result = s.numEnclaves(grid)
print(result)  # 3
