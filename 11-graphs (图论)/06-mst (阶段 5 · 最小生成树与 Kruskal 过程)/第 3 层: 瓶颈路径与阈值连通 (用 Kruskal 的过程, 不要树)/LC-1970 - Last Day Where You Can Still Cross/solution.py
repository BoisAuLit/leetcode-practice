"""LC-1970 - Last Day Where You Can Still Cross

阶段 5 · 最小生成树与 Kruskal 过程 · 第 3 层: 瓶颈路径与阈值连通 (用 Kruskal 的过程, 不要树) ○ 核心
题目在问：row x col 的陆地, 第 i 天 cells[i-1] 那格变成水, 最后哪一天还能只走陆地 (四方向) 从第一行走到最后一行
点是什么：每个格子 + 虚拟"顶"点 + 虚拟"底"点   边是什么：上下左右相邻的陆地; 第一行的陆地连顶, 最后一行的陆地连底
和签名题比改了哪一行：1697 是"门槛从小到大, 边越加越多"; 这里格子是被删掉的, 并查集不会拆, 所以时间倒放:
                     先假设全淹完, 从最后一天往前把格子"抽干"加回来, 顶和底第一次连通的那天就是答案
"""
from collections import deque
from typing import List


class UnionFind:  # 路径减半 + 按 size 合并, 和 1135 / 1584 一样
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
##### ! Solution 1: 时间倒放 + 并查集 + 虚拟顶/底点
##### ! 时间复杂度: O(row · col · α(row · col))   空间复杂度: O(row · col)
##### ! 适用："东西随时间被删, 问最后能撑到何时"; 倒着看就是逐个加入, 并查集只合并不拆分
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def latestDayToCross(self, row: int, col: int, cells: List[List[int]]) -> int:
        TOP, BOT = row * col, row * col + 1  # 两个虚拟点, 排在所有格子后面
        uf = UnionFind(row * col + 2)
        land = [False] * (row * col)  # 一开始假设全淹完, 全是水

        for day in range(len(cells) - 1, -1, -1):  # ! 时间倒放: 从最后一天往前抽干
            r, c = cells[day][0] - 1, cells[day][1] - 1  # 题目是 1-indexed
            idx = r * col + c
            land[idx] = True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 和已经是陆地的邻居接上
                nr, nc = r + dr, c + dc
                if 0 <= nr < row and 0 <= nc < col and land[nr * col + nc]:
                    uf.union(idx, nr * col + nc)
            if r == 0:
                uf.union(idx, TOP)
            if r == row - 1:
                uf.union(idx, BOT)
            # ! 顶底第一次连通: cells[day] 抽干后能过, 也就是只淹了 cells[0..day-1] 的"第 day 天"还能过
            if uf.find(TOP) == uf.find(BOT):
                return day
        return 0  # 理论上到不了这里 (第 0 天没淹任何格子, 一定能过)


##################################################################################################
##### ! Solution 2: 二分天数 + BFS 检查通不通
##### ! 时间复杂度: O(row · col · log(row · col))   空间复杂度: O(row · col)
##### ! 适用：答案满足"天数越大越难过"时的通用做法; 不需要并查集, 面试时作为第二种思路
##################################################################################################


class Solution_2:
    def latestDayToCross(self, row: int, col: int, cells: List[List[int]]) -> int:
        def can_cross(day: int) -> bool:  # 淹了 cells[0..day-1] 之后还能不能从第一行走到最后一行
            water = [[False] * col for _ in range(row)]
            for r, c in cells[:day]:
                water[r - 1][c - 1] = True
            q = deque()
            for c in range(col):  # ! 第一行所有陆地一起当起点 (多源 BFS)
                if not water[0][c]:
                    water[0][c] = True  # water 顺便当 visited 用
                    q.append((0, c))
            while q:
                r, c = q.popleft()
                if r == row - 1:
                    return True
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < row and 0 <= nc < col and not water[nr][nc]:
                        water[nr][nc] = True
                        q.append((nr, nc))
            return False

        lo, hi = 0, len(cells)  # ! 第 0 天一定能过; 找最大的还能过的 day
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can_cross(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo


s = Solution_1()
row, col = 2, 2
cells = [[1, 1], [2, 1], [1, 2], [2, 2]]
result = s.latestDayToCross(row, col, cells)
print(result)  # 2
