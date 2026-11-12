"""LC-1489 - Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree

阶段 5 · 最小生成树与 Kruskal 过程 · 第 2 层 追问 MST 结构(只能用 Kruskal 做) ○ 核心
题目在问：给 n 个点和边表 [u, v, w]，哪些边是每棵 MST 都必须含的(关键边)，哪些边"有的 MST 含、有的不含"(伪关键边)
点是什么：n 个点   边是什么：edges 里的每条，价格 = w；答案要的是边的下标，所以排序要排"下标"
和签名题(1584)比改了哪一行：Kruskal 的循环里多两个开关
  skip  = 排除实验：这条边当作不存在，总价变大或连不起来 → 关键边
  force = 强制实验：开跑前先把这条边买下，总价仍等于 base → 存在一棵含它的 MST → 伪关键边(前提：它没通过关键边检验)
"""
from math import inf
from typing import List


##################################################################################################
##### ! Solution 1: Kruskal 跑三遍：正常 / 排除实验 (skip) / 强制实验 (force)
##### ! 时间复杂度: O(E log E + E² · α(n)) = O(E² α)   空间复杂度: O(n + E)   排序一次，每条边各跑两次 Kruskal
##### ! 适用：追问"哪条边必须要、哪条可有可无"只能用 Kruskal：它有"逐条审批边"的环节，能跳过、能先买；
##### !       Prim 是"圈子长大"，没有审批某条边的时机，做不了
##### ! 只写这一种：E ≤ 100，每条边跑两次 Kruskal 绰绰有余；O(E α) 的"按同权边分组 + Tarjan 求桥"写法面试不会要求
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
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


class Solution_1:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # ! 排的是"边的下标"不是边本身：答案要下标
        order = sorted(range(len(edges)), key=lambda i: edges[i][2])

        def mst_cost(skip: int = -1, force: int = -1) -> int:
            uf = UnionFind(n)
            total = used = 0
            if force != -1:  # ! 强制实验：循环开始之前就把这条边买下，它百分之百在树里
                u, v, w = edges[force]
                uf.union(u, v)
                total += w
                used += 1
            for i in order:
                if i == skip:  # ! 排除实验：这条边当作不存在
                    continue
                u, v, w = edges[i]
                if uf.union(u, v):
                    total += w
                    used += 1
            return total if used == n - 1 else inf  # 连不起来 = 无穷大，自然比 base 大

        base = mst_cost()  # 正常跑一遍，拿到最小总价
        critical, pseudo = [], []
        for i in range(len(edges)):
            if mst_cost(skip=i) > base:  # 没有它就达不到最小(或直接断开)
                critical.append(i)
            elif mst_cost(force=i) == base:  # 先买它再跑 = "所有含它的生成树里最便宜的"，等于 base 就说明有一棵 MST 含它
                pseudo.append(i)
        return [critical, pseudo]


s = Solution_1()
n = 5
edges = [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]]
result = s.findCriticalAndPseudoCriticalEdges(n, edges)
print(result)  # [[0, 1], [2, 3, 4, 5]]

n = 4
edges = [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]]
result = s.findCriticalAndPseudoCriticalEdges(n, edges)
print(result)  # [[], [0, 1, 2, 3]]
