"""LC-2316 - Count Unreachable Pairs of Nodes in an Undirected Graph

阶段 2 · 并查集计数 (块数 = n - 成功合并次数) ○ 核心变体
题目在问：n 个点、若干无向边，互相到不了的点对有几对
点是什么：节点 0..n-1   边是什么：edges 里的无向边
和签名题比改了哪一行：323 只数"有几派"；这里要知道"每派多大"，把 size 数组拿出来，各派 size 两两相乘
"""
from collections import deque
from typing import List


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
##### ! Solution 1: Union-Find with size
##### ! 时间复杂度: O((n + E) · α(n))   空间复杂度: O(n)
##### ! 适用：边列表直接喂并查集，不用建邻接表；size 数组现成，最短最常考
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def countPairs(self, n: int, edges: List[List[int]]) -> int:
        uf = UnionFind(n)
        for a, b in edges:
            uf.union(a, b)

        # ! 画面：各派一派一派走上台，新上台的一派和已经在台上的所有人两两配对
        ans = on_stage = 0
        for i in range(n):
            if uf.find(i) == i:  # 只看根，根的 size 才是整派人数
                sz = uf.size[i]
                ans += sz * on_stage
                on_stage += sz
        return ans


##################################################################################################
##### ! Solution 2: BFS component sizes
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n + E)
##### ! 适用：静态图数每块大小的标准写法；换个公式：总对数 C(n,2) 减去各派内部的 C(sz,2)
##################################################################################################


class Solution_2:
    def countPairs(self, n: int, edges: List[List[int]]) -> int:
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        ans = n * (n - 1) // 2  # 先当所有点对都不可达
        visited = [False] * n
        for s in range(n):
            if visited[s]:
                continue
            visited[s] = True
            q = deque([s])
            sz = 0
            while q:  # n 到 1e5，用队列不用递归
                u = q.popleft()
                sz += 1
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        q.append(v)
            ans -= sz * (sz - 1) // 2  # ! 同一派内部的点对其实可达，扣掉
        return ans


s = Solution_1()
n = 7
edges = [[0, 2], [0, 5], [2, 4], [1, 6], [5, 4]]
result = s.countPairs(n, edges)
print(result)  # 14
print(Solution_1().countPairs(3, [[0, 1], [0, 2], [1, 2]]))  # 0
