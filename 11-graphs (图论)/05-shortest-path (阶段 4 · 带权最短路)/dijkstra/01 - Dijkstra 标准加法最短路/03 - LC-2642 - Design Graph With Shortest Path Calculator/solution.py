"""LC-2642 - Design Graph With Shortest Path Calculator

阶段 4 · Dijkstra 堆版 (relax 写 d + w) △ 扩展
题目在问：有向带权图，支持随时加一条边、随时问两点之间的最短路，不可达返回 -1
点是什么：0..n-1   边是什么：有向边 (from, to, cost)，会动态增加
和签名题比改了哪一行：743 跑一次 Dijkstra 取 dist 的最大值；这里每次 shortestPath 跑一次 Dijkstra 只取 dist[node2]，
邻接表变成成员变量，addEdge 就是往里 append 一条
"""
from heapq import heappop, heappush
from math import inf
from typing import List

##################################################################################################
##### ! Solution 1: Dijkstra per query
##### ! 时间复杂度: __init__ O(n + E)，addEdge O(1)，shortestPath O(E log n)   空间复杂度: O(n + E)
##### ! 适用：加边多、查询少，或图大到放不下 n^2 的表；也是手册点名的标准写法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Graph_1:
    def __init__(self, n: int, edges: List[List[int]]):
        self.n = n
        self.adj = [[] for _ in range(n)]
        for u, v, w in edges:
            self.adj[u].append((v, w))  # 有向，只存一边

    def addEdge(self, edge: List[int]) -> None:
        u, v, w = edge
        self.adj[u].append((v, w))  # ! 加边只是 append，什么都不用重算

    def shortestPath(self, node1: int, node2: int) -> int:
        dist = [inf] * self.n
        dist[node1] = 0
        heap = [(0, node1)]  # (距离, 点)
        while heap:
            d, u = heappop(heap)
            if u == node2:  # ! 第一次弹到终点就是答案，堆里剩下的都不比它近
                return d
            if d > dist[u]:  # 作废票
                continue
            for v, w in self.adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heappush(heap, (d + w, v))
        return -1  # 堆空了还没弹到 node2：到不了


##################################################################################################
##### ! Solution 2: Floyd matrix maintained incrementally
##### ! 时间复杂度: __init__ O(n^3)，addEdge O(n^2)，shortestPath O(1)   空间复杂度: O(n^2)
##### ! 适用：n ≤ 100、查询远多于加边；一张表养着，加边时只用新边松弛一遍所有点对
##################################################################################################


class Graph_2:
    def __init__(self, n: int, edges: List[List[int]]):
        self.n = n
        dist = [[inf] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:
            if w < dist[u][v]:  # 重边取小
                dist[u][v] = w
        for k in range(n):  # 1334 的 Floyd 原样
            dk = dist[k]
            for i in range(n):
                dik = dist[i][k]
                if dik == inf:
                    continue
                di = dist[i]
                for j in range(n):
                    if dik + dk[j] < di[j]:
                        di[j] = dik + dk[j]
        self.dist = dist

    def addEdge(self, edge: List[int]) -> None:
        u, v, w = edge
        dist = self.dist
        if dist[u][v] <= w:  # 原来 u 到 v 已经不比新边贵，新边没用
            return
        # ! 权非负，新最短路最多用这条新边一次，所以一定长成 i -> ... -> u -> v -> ... -> j
        # ! 只需用 dist[i][u] + w + dist[v][j] 松弛一遍所有 (i, j)，不用重跑 n^3
        dv = dist[v]
        for i in range(self.n):
            diu = dist[i][u]
            if diu == inf:
                continue
            di = dist[i]
            for j in range(self.n):
                if diu + w + dv[j] < di[j]:
                    di[j] = diu + w + dv[j]

    def shortestPath(self, node1: int, node2: int) -> int:
        d = self.dist[node1][node2]
        return -1 if d == inf else d


g = Graph_1(4, [[0, 2, 5], [0, 1, 2], [1, 2, 1], [3, 0, 3]])
print(g.shortestPath(3, 2))  # 6
print(g.shortestPath(0, 3))  # -1
g.addEdge([1, 3, 4])
print(g.shortestPath(0, 3))  # 6
