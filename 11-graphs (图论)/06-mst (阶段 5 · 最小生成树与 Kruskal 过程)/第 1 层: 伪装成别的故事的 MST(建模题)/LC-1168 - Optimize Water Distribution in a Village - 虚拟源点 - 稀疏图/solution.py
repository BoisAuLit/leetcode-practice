"""LC-1168 - Optimize Water Distribution in a Village

阶段 5 · 最小生成树与 Kruskal 过程 · 第 1 层 伪装成别的故事的 MST(虚拟源点，稀疏图) ○ 核心
题目在问：n 户人家，每家要么自己打井(wells[i-1])，要么用水管接到有水的邻居(pipes)，每家都有水最少花多少
点是什么：n 户 + 一个 0 号虚拟"水源"   边是什么：水管 = 普通边；打井 = 0 和 i 之间一条价格 wells[i-1] 的边
和签名题(1584)比改了哪一行：多加一个虚拟源点 0，把"自建"翻成"到 0 的边"，然后在 n+1 个点上跑普通 MST；
  图一定连通(每家都能直接接到 0)，所以不用判 -1；三个解法都直接往 pipes 里 append 井边
"""
from typing import List
from heapq import heappush, heappop
from math import inf


##################################################################################################
##### ! Solution 1: Prim with Array
##### ! 时间复杂度: O(n² + E)   空间复杂度: O(n + E)   E = len(pipes) + n(井边)，n+1 个点
##### ! This is the preferred solution
##### ! Prim 的 array 版本适用于稠密图
##################################################################################################
class Solution_1:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        for i, w in enumerate(wells):
            pipes.append((0, i + 1, w))
        adj = [[] for _ in range(n + 1)]
        for u, v, w in pipes:
            adj[u].append((v, w))
            adj[v].append((u, w))
        in_tree = [False] * (n + 1)
        min_dist = [inf] * (n + 1)
        min_dist[0] = 0
        total = 0
        for _ in range(n + 1):
            u = -1
            for j in range(n + 1):
                if not in_tree[j] and (u == -1 or min_dist[j] < min_dist[u]):
                    u = j
            in_tree[u] = True
            total += min_dist[u]
            for v, w in adj[u]:
                if not in_tree[v]:
                    min_dist[v] = min(min_dist[v], w)
        return total


##################################################################################################
##### ! Solution 2: Prim with heap
##### ! 时间复杂度: O(E log E)   空间复杂度: O(n + E)   稀疏图(pipes ≤ 1e4)用堆版，不用扫 n 个标价牌
##### ! Prim 的 heap 版本适用于稀疏图
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        for i, w in enumerate(wells):
            pipes.append((0, i + 1, w))
        adj = [[] for _ in range(n + 1)]
        for u, v, w in pipes:
            adj[u].append((v, w))
            adj[v].append((u, w))
        in_tree = [False] * (n + 1)
        heap = [(0, 0)]
        total = 0
        while heap:
            w, u = heappop(heap)
            if in_tree[u]:
                continue
            total += w
            in_tree[u] = True
            for v, wt in adj[u]:
                if not in_tree[v]:
                    heappush(heap, (wt, v))
        return total


##################################################################################################
##### ! Solution 3: Kruskal
##### ! 时间复杂度: O(E log E)   空间复杂度: O(n + E)   瓶颈是排序；买够 n 条边(n+1 个点)就停
##### ! 本版本适用于稀疏图
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################6+++++++++++0.

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


class Solution:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        uf = UnionFind(n + 1)
        for i, v in enumerate(wells):
            pipes.append((0, i + 1, v))
        pipes.sort(key=lambda t: t[2])
        total = 0
        used = 0
        for u, v, w in pipes:
            if uf.union(u, v):
                total += w
                used += 1
                if used == n:
                    break

        return total


s = Solution_2()
n = 3
wells = [1, 2, 2]
pipes = [[1, 2, 1], [2, 3, 1]]
result = s.minCostToSupplyWater(n, wells, pipes)
print(result)  # 3

n = 2
wells = [1, 1]
pipes = [[1, 2, 1], [1, 2, 2]]
result = s.minCostToSupplyWater(n, wells, pipes)
print(result)  # 2
