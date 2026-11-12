"""LC-1102 - Path With Maximum Minimum Value

阶段 4 · 瓶颈路径 (relax 改 max 或 min) ○ 核心题
题目在问：网格每格有个值，一条路径的分数是路径上的最小值，从左上走到右下(四方向)分数最大是多少 (maximin)
点是什么：一个格子   边是什么：上下左右相邻，"价格"写在格子上
和签名题比改了哪一行：743 的 relax 是 d + w 取小；这里改成 min(d, w) 取大，配大根堆(标签取负)
手册第三层 / 第四层：778、1631、1102 同一批题，三种解法都要会说：
  Dijkstra 改 relax (单起点单终点，代码最短) / Kruskal 过程 + 并查集 (多查询、离线、倒放时间) / 二分答案 + BFS (最直白)
"""
from collections import deque
from heapq import heappop, heappush
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class UnionFind:  # 和 1135 完全一样：路径减半 + 按 size 合并，union 返回有没有真的合并
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
##### ! Solution 1: Dijkstra 骨架，relax 改成 min(d, w) + 大根堆
##### ! 时间复杂度: O(mn log(mn))   空间复杂度: O(mn)
##### ! 适用：单起点单终点，三种解法里代码最短；标签 = 到这格为止路径上的最小值，每次弹最大的那个定案
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maximumMinimumPath(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        best = [[-1] * n for _ in range(m)]  # ! 到这格为止"路径最小值"的最大值，初值 -1 (对应 743 的 inf)
        best[0][0] = grid[0][0]
        heap = [(-grid[0][0], 0, 0)]  # ! (负的路径最小值, r, c)，取负让 heapq 变成大根堆

        while heap:
            neg, r, c = heappop(heap)
            d = -neg
            if (r, c) == (m - 1, n - 1):  # 第一次弹出终点就是答案
                return d
            if d < best[r][c]:  # 作废票
                continue
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nd = min(d, grid[nr][nc])  # ! relax 写 min，不是 d + w
                    if nd > best[nr][nc]:  # ! 比旧标签大才更新 (maximin，方向和 743 反过来)
                        best[nr][nc] = nd
                        heappush(heap, (-nd, nr, nc))

        return -1  # 网格总是连通的，不会走到这里


##################################################################################################
##### ! Solution 2: Kruskal 过程 (格子按值从大到小开放 + 并查集，不要那棵树)
##### ! 时间复杂度: O(mn log(mn)) 排序为主，并查集近似 O(1)   空间复杂度: O(mn)
##### ! 适用：门槛 x 从高往低降，问"只走 >= x 的格子通不通"；多组查询 / 离线 / 时间倒放时只能用这个
##################################################################################################


class Solution_2:
    def maximumMinimumPath(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        cells = sorted(range(m * n), key=lambda i: grid[i // n][i % n], reverse=True)  # ! 格子按值从大到小排队
        uf = UnionFind(m * n)
        opened = [False] * (m * n)
        src, dst = 0, m * n - 1

        for i in cells:
            opened[i] = True  # ! 门槛降到 grid 值，这格开放
            r, c = divmod(i, n)
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and opened[nr * n + nc]:
                    uf.union(i, nr * n + nc)  # 和已开放的邻居合并，返回值无所谓，只记连通性
            if opened[src] and opened[dst] and uf.find(src) == uf.find(dst):  # ! 左上右下第一次连通
                return grid[r][c]  # 此刻的门槛就是答案

        return -1


##################################################################################################
##### ! Solution 3: 二分答案 + BFS 检查
##### ! 时间复杂度: O(mn log(mn))，二分不同值的个数，每次 BFS O(mn)   空间复杂度: O(mn)
##### ! 适用：最直白、最好解释；门槛越低越容易通，所以"能不能通"随 x 只翻一次，可以二分
##################################################################################################


class Solution_3:
    def maximumMinimumPath(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        def ok(x: int) -> bool:  # ! 只走值 >= x 的格子，左上能不能到右下
            if grid[0][0] < x:
                return False
            seen = [[False] * n for _ in range(m)]
            seen[0][0] = True
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if (r, c) == (m - 1, n - 1):
                    return True
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and not seen[nr][nc] and grid[nr][nc] >= x:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            return False

        vals = sorted({v for row in grid for v in row})  # 答案一定是格子里出现过的值
        lo, hi = 0, len(vals) - 1  # ! 找最大的下标使 ok 为真；vals[0] 是全局最小值，必通
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if ok(vals[mid]):
                lo = mid
            else:
                hi = mid - 1
        return vals[lo]


s = Solution_1()
grid = [[5, 4, 5], [1, 2, 6], [7, 4, 6]]
result = s.maximumMinimumPath(grid)
print(result)  # 4

grid = [[2, 2, 1, 2, 2, 2], [1, 2, 2, 2, 1, 2]]
result = s.maximumMinimumPath(grid)
print(result)  # 2

grid = [[3, 4, 6, 3, 4], [0, 2, 1, 1, 7], [8, 8, 3, 2, 7], [3, 2, 4, 9, 8], [4, 1, 2, 0, 0], [4, 6, 5, 4, 3]]
result = s.maximumMinimumPath(grid)
print(result)  # 3
