"""LC-1559 - Detect Cycles in 2D Grid

阶段 2 · 并查集成环 (union 返回 False) △ 扩展
题目在问：m x n 字符网格，相同字符的格子能不能走出一个长度 >= 4、不许原路掉头的环
点是什么：每个格子   边是什么：上下左右相邻且字符相同
和签名题比改了哪一行：684 的边是列表给的，逐条 union，第一次失败的那条就是答案；
                      这里的边要自己从网格里生成 (每格只看右边和下边，一条边只碰一次)，union 失败就 return True
"""
from collections import deque
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
##### ! Solution 1: Union-Find，union 失败即成环
##### ! 时间复杂度: O(m·n · α(m·n))   空间复杂度: O(m·n)
##### ! 适用：最短；网格是二分图没有三角形，所以"有环"自动就是"环长 >= 4"，不用额外判长度
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def containsCycle(self, grid: List[List[str]]) -> bool:
        m, n = len(grid), len(grid[0])
        uf = UnionFind(m * n)  # 格子 (r, c) 编号 r*n + c
        for r in range(m):
            for c in range(n):
                ch = grid[r][c]
                # ! 只看右边和下边：每条无向边恰好碰一次，不会"同一条边 union 两遍"造成假成环
                if c + 1 < n and grid[r][c + 1] == ch:
                    if not uf.union(r * n + c, r * n + c + 1):
                        return True
                if r + 1 < m and grid[r + 1][c] == ch:
                    if not uf.union(r * n + c, (r + 1) * n + c):
                        return True
        return False


##################################################################################################
##### ! Solution 2: DFS 带父亲 (迭代)
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：无向图判环的经典 DFS：碰到"已访问但不是父亲"的邻居就是环；500x500 用栈不用递归
##################################################################################################


class Solution_2:
    def containsCycle(self, grid: List[List[str]]) -> bool:
        m, n = len(grid), len(grid[0])
        visited = [[False] * n for _ in range(m)]
        for sr in range(m):
            for sc in range(n):
                if visited[sr][sc]:
                    continue
                visited[sr][sc] = True
                stack = [(sr, sc, -1, -1)]  # (当前格, 它是从哪格走来的)
                while stack:
                    r, c, pr, pc = stack.pop()
                    ch = grid[r][c]
                    for dr, dc in DIRS:
                        nr, nc = r + dr, c + dc
                        if not (0 <= nr < m and 0 <= nc < n) or grid[nr][nc] != ch:
                            continue
                        if (nr, nc) == (pr, pc):  # ! 不许掉头回上一格
                            continue
                        if visited[nr][nc]:  # ! 不是父亲却已经见过：绕回来了
                            return True
                        visited[nr][nc] = True  # 入栈时就标记，同一格不会被两边各推一次
                        stack.append((nr, nc, r, c))
        return False


##################################################################################################
##### ! Solution 3: 数每块的点数和边数 (BFS)
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：换个角度看同一件事：一块连通块若是树则 E = V - 1，所以 E >= V 就有环；和 Solution 1 的"失败次数 > 0"等价
##################################################################################################


class Solution_3:
    def containsCycle(self, grid: List[List[str]]) -> bool:
        m, n = len(grid), len(grid[0])
        visited = [[False] * n for _ in range(m)]
        for sr in range(m):
            for sc in range(n):
                if visited[sr][sc]:
                    continue
                ch = grid[sr][sc]
                visited[sr][sc] = True
                q = deque([(sr, sc)])
                V = E = 0
                while q:
                    r, c = q.popleft()
                    V += 1
                    for dr, dc in DIRS:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == ch:
                            E += 1  # 每条边会从两头各数一次
                            if not visited[nr][nc]:
                                visited[nr][nc] = True
                                q.append((nr, nc))
                if E // 2 >= V:  # ! 边数 >= 点数：不是树，有环
                    return True
        return False


s = Solution_1()
grid = [["a", "a", "a", "a"], ["a", "b", "b", "a"], ["a", "b", "b", "a"], ["a", "a", "a", "a"]]
result = s.containsCycle(grid)
print(result)  # True
print(Solution_1().containsCycle([["c", "c", "c", "a"], ["c", "d", "c", "c"], ["c", "c", "e", "c"], ["f", "c", "c", "c"]]))  # True
print(Solution_1().containsCycle([["a", "b", "b"], ["b", "z", "b"], ["b", "b", "a"]]))  # False
