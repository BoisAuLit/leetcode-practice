"""LC-0827 - Making A Large Island

阶段 2 · 并查集建模 (把别的东西当点) △ 扩展
题目在问：n x n 的 0/1 网格，最多把一个 0 翻成 1，最大的岛能有多大
点是什么：每个格子   边是什么：上下左右相邻且都是 1
和签名题比改了哪一行：305 是"真的加一个点，报岛数"；这里是"试着加每一个 0，报最大面积"，
                      所以先给每块岛编号并记下 size，再枚举每个 0，把四周"不同编号"的岛 size 加起来 + 1
"""
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class UnionFind:  # 路径减半 + 按 size 合并，union 返回 bool
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


##################################################################################################
##### ! Solution 1: DFS 染色 + 枚举每个 0
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)
##### ! 适用：静态网格，一遍染色把每块岛的编号和面积记好，枚举 0 时 O(1) 查表；最常考
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def largestIsland(self, grid: List[List[int]]) -> int:
        n = len(grid)
        area = {}  # 岛编号 -> 面积
        color = 2  # ! 编号从 2 开始，和 0/1 不撞车；直接写进 grid，grid 就是 visited

        for r in range(n):
            for c in range(n):
                if grid[r][c] != 1:
                    continue
                stack = [(r, c)]  # 用栈不用递归：500x500 全 1 时递归深度 25 万会爆栈
                grid[r][c] = color
                sz = 0
                while stack:
                    x, y = stack.pop()
                    sz += 1
                    for dx, dy in DIRS:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 1:
                            grid[nx][ny] = color
                            stack.append((nx, ny))
                area[color] = sz
                color += 1

        # ! 全 1 时没有 0 可翻，答案就是唯一那块岛 (= n*n)；只要有 0，下面一定能更新到更大
        best = max(area.values(), default=0)
        for r in range(n):
            for c in range(n):
                if grid[r][c] != 0:
                    continue
                seen = set()  # ! 同一块岛从两边贴着这个 0，面积只能加一次
                total = 1
                for dx, dy in DIRS:
                    nx, ny = r + dx, c + dy
                    if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] > 1:
                        cid = grid[nx][ny]
                        if cid not in seen:
                            seen.add(cid)
                            total += area[cid]
                best = max(best, total)
        return best


##################################################################################################
##### ! Solution 2: Union-Find + 枚举每个 0
##### ! 时间复杂度: O(n^2 · α(n^2))   空间复杂度: O(n^2)
##### ! 适用：不想改 grid 时用；岛的面积就是根的 size，不用自己记 area 表
##################################################################################################


class Solution_2:
    def largestIsland(self, grid: List[List[int]]) -> int:
        n = len(grid)
        uf = UnionFind(n * n)  # 格子 (r, c) 编号 r*n + c
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    continue
                if c + 1 < n and grid[r][c + 1] == 1:  # 只看右边和下边，每条边 union 一次
                    uf.union(r * n + c, r * n + c + 1)
                if r + 1 < n and grid[r + 1][c] == 1:
                    uf.union(r * n + c, (r + 1) * n + c)

        best = 0
        for i in range(n * n):  # 全 1 的兜底：最大的岛本身
            if grid[i // n][i % n] == 1:
                best = max(best, uf.size[uf.find(i)])
        for r in range(n):
            for c in range(n):
                if grid[r][c] != 0:
                    continue
                seen = set()
                total = 1
                for dx, dy in DIRS:
                    nx, ny = r + dx, c + dy
                    if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 1:
                        root = uf.find(nx * n + ny)  # ! 用根当岛的身份证，size[root] 就是面积
                        if root not in seen:
                            seen.add(root)
                            total += uf.size[root]
                best = max(best, total)
        return best


s = Solution_1()
grid = [[1, 0], [0, 1]]
result = s.largestIsland(grid)
print(result)  # 3
print(Solution_1().largestIsland([[1, 1], [1, 0]]))  # 4
print(Solution_1().largestIsland([[1, 1], [1, 1]]))  # 4
