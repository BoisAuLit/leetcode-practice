"""LC-1135 - Connecting Cities With Minimum Cost

阶段 5 · 最小生成树与 Kruskal 过程 · 第 1 层 伪装成别的故事的 MST(稀疏图) ○ 核心
题目在问：n 座城市(编号 1..n)和一张可修道路清单 [a, b, 费用]，把所有城市连通最少花多少；连不起来 -1
点是什么：城市   边是什么：清单里的道路，价格 = 费用
和签名题(1584)比改了哪一行：边从"完全图现算"变成"给定的稀疏边表"；编号从 1 开始要多开一格；
  可能不连通：Kruskal 看 used < n-1、Prim 堆版看 count < n、数组版看 min_dist == inf
"""
from heapq import heappush, heappop
from math import inf

##################################################################################################
##### ! Solution 1: Prim with Array
##### ! 时间复杂度: O(n² + E)   空间复杂度: O(n + E)   每轮扫一遍 n 个标价牌，降价只看邻接表
##### ! This is the preferred solution
##### ! Prim 的 array 版本适用于稠密图
##################################################################################################

class Solution_1:
    def minimumCost(self, n: int, connections: list[list[int]]) -> int:
        adj = [[] for _ in range(n + 1)]
        for u, v, w in connections:
            adj[u].append((v, w))
            adj[v].append((u, w))

        in_tree = [False] * (n + 1)
        min_dist = [inf] * (n + 1)
        min_dist[1] = 0  # 从 1 号城市起步
        total = 0

        for _ in range(n):
            # 看牌:在圈外的城市里找标价最低的(只扫 1..n,0 号那格不看)
            u = -1
            for j in range(1, n + 1):
                if not in_tree[j] and (u == -1 or min_dist[j] < min_dist[u]):
                    u = j
            # 卡住:最便宜的也是 inf → 圈外没人和圈内有线 → 不连通
            if min_dist[u] == inf:
                return -1
            # 买线
            in_tree[u] = True
            total += min_dist[u]
            # 降价:只看 u 的邻居,稀疏图没必要扫全部
            for v, w in adj[u]:
                if not in_tree[v]:
                    min_dist[v] = min(min_dist[v], w)

        return total


##################################################################################################
##### ! Solution 2: Prim with heap
##### ! 时间复杂度: O(E log E)   空间复杂度: O(n + E)   每条边最多扔一张票进堆
##### ! Prim 的 heap 版本适用于稀疏图
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def minimumCost(self, n: int, connections: list[list[int]]) -> int:
        adj = [[] for _ in range(n + 1)]  # 多开一格,城市 1..n 直接当下标
        for u, v, w in connections:
            adj[u].append((v, w))
            adj[v].append((u, w))  # 无向图两边都存

        in_tree = [False] * (n + 1)
        heap = [(0, 1)]  # (价格, 城市),从 1 号起步,0 元
        total = count = 0

        while heap and count < n:  # 没票了 / 买够 n 个就停
            w, u = heappop(heap)  # 看牌
            if in_tree[u]:  # 作废票
                continue
            in_tree[u] = True  # 买线
            total += w
            count += 1
            for v, wt in adj[u]:  # 扔票
                if not in_tree[v]:
                    heappush(heap, (wt, v))

        return total if count == n else -1  # 没买够 n 个 → 不连通


##################################################################################################
##### ! Solution 3: Kruskal
##### ! 时间复杂度: O(E log E)   空间复杂度: O(n + E)   瓶颈是排序，并查集近似 O(1)
##### ! 本版本适用于稀疏图
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class UnionFind:  # 和 1584 完全一样,一个字都不改
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
    def minimumCost(self, n: int, connections: list[list[int]]) -> int:
        connections.sort(key=lambda c: c[2])
        uf = UnionFind(n + 1)  # 多开一格:下标 0 闲置,城市 1..n 直接用
        total = used = 0
        for u, v, w in connections:
            if uf.union(u, v):
                total += w
                used += 1
                if used == n - 1:
                    break
        return total if used == n - 1 else -1


s = Solution_1()
n = 3
connections = [[1, 2, 5], [1, 3, 6], [2, 3, 1]]
result = s.minimumCost(n, connections)
print(result)
