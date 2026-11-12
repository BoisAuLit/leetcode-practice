# https://leetcode.com/problems/min-cost-to-connect-all-points/
"""LC-1584 - Min Cost to Connect All Points

阶段 5 · 最小生成树与 Kruskal 过程 · 第 1 层 纯粹的 MST(稠密图) ★ 签名题
题目在问：平面上 n 个点，任意两点可拉线，费用是曼哈顿距离，把所有点连通最少花多少
点是什么：坐标点   边是什么：任意两点之间都有线(完全图，E = n(n-1)/2)，价格 = |x1-x2| + |y1-y2|
和签名题比改了哪一行：本题就是签名题；完全图不用把边造出来，Prim 数组版 O(n²) 最合适
三种写法都要盲写：Prim 数组版 / Prim 堆版 / Kruskal + 并查集
"""

##################################################################################################
##### ! Solution 1: Prim with Array
##### ! 时间复杂度: O(n²)   空间复杂度: O(n)   完全图 E ≈ n²/2，数组版不用造边不用排序，正好
##### ! This is the preferred solution
##### ! Prim 的 array 版本适用于稠密图
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

from typing import List
from math import inf
from heapq import heappush, heappop

# Time:  O(n²)   每轮扫一遍标价牌 O(n),一共 n 轮;不用造边、不用排序
# Space: O(n)


class Solution_1:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        in_tree = [False] * n
        min_dist = [inf] * n
        min_dist[0] = 0
        total = 0

        def manhattan(p: List[int], q: List[int]) -> int:
            return abs(p[0] - q[0]) + abs(p[1] - q[1])

        for _ in range(n):
            # 看牌
            u = -1
            for j in range(n):
                # 找到目前最小的价格
                if not in_tree[j] and (u == -1 or min_dist[j] < min_dist[u]):
                    u = j
            # 买线
            in_tree[u] = True
            total += min_dist[u]
            # 降价
            for j in range(n):
                if not in_tree[j]:
                    d = manhattan(points[u], points[j])
                    min_dist[j] = min(min_dist[j], d)

        return total


##################################################################################################
##### ! Solution 2: Prim with heap
##### ! 时间复杂度: O(n² log n)   空间复杂度: O(n²)   完全图每根线都要扔票进堆，比数组版多一个 log
##### ! Prim 的 heap 版本适用于稀疏图
##################################################################################################

# Time:  O(E log E) = O(n² log n)   每根线最多扔一张票进堆
# Space: O(E)



class Solution_2:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        in_tree = [False] * n
        heap = [(0, 0)]                    # (价格, 门牌号),起点 0 元
        total = count = 0

        while count < n:
            w, u = heappop(heap)           # 看牌
            if in_tree[u]:                 # 作废票
                continue
            in_tree[u] = True              # 买线
            total += w
            count += 1
            for v in range(n):             # 扔票:完全图,给每个圈外的点一张
                if not in_tree[v]:
                    d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                    heappush(heap, (d, v))

        return total


##################################################################################################
##### ! Solution 3: Kruskal
##### ! 时间复杂度: O(n² log n)   空间复杂度: O(n²)   得先把 n²/2 条边造出来排序
##### ! Kruskal 适用于稀疏图
##################################################################################################


# Time:  O(E log E),E = n(n-1)/2  →  O(n² log n)   瓶颈是排序
# Space: O(E)  要把所有边存下来排序


class UnionFind:
    """只负责一件事:两个人是不是一派,不是就合并。算法层的账(总价、边数)不放这里。"""

    def __init__(self, n: int):
        self.parent = list(range(n))  # 每个人一开始自己当老大
        self.size = [1] * n  # 每派人数(只在老大身上有意义)

    def find(self, x: int) -> int:
        """找 x 的老大,顺手把路走短(路径减半:认爷爷,跳过父亲)"""
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        """返回 True = 真的合并了;False = 本来就是一派(在 Kruskal 里 = 这条边会成环)"""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:  # 小派并入大派,链条不会长高
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


class Solution_3:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)

        def manhattan(p: List[int], q: List[int]) -> int:
            return abs(p[0] - q[0]) + abs(p[1] - q[1])

        # 造边:完全图,每对点一条边;元组把价格放第一位,方便直接 sort()
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                edges.append((manhattan(points[i], points[j]), i, j))

        edges.sort()  # ① 排队:按价格从便宜到贵
        uf = UnionFind(n)
        total = 0
        used = 0
        for w, u, v in edges:
            if uf.union(u, v):  # ② 问:两头还没连通 → ③ 买
                total += w
                used += 1
                if used == n - 1:  # 买够 n-1 条就是一棵树,提前收工
                    break

        # 只有 1 个点时 edges 为空,used == 0 == n-1,自然返回 0,不需要特判
        return total


s = Solution_1()
points = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]
result = s.minCostConnectPoints(points)
print(result)  # 20
