"""LC-1976 - Number of Ways to Arrive at Destination

阶段 4 · Dijkstra 堆版 (relax 写 d + w) ○ 核心题
题目在问：n 个路口、双向带时间的路，从 0 到 n - 1 用时最短的走法有几种，答案对 1e9 + 7 取模
点是什么：路口   边是什么：roads[i] = [u, v, time]，无向
和签名题比改了哪一行：743 的 Dijkstra 原样保留，多一个 ways 数组：
  relax 时严格更小就覆盖 ways[v] = ways[u]，相等就累加 ways[v] += ways[u]
"""
from heapq import heappop, heappush
from math import inf
from typing import List

MOD = 10**9 + 7

##################################################################################################
##### ! Solution 1: Dijkstra + ways 数组 (一遍跑完)
##### ! 时间复杂度: O((V + E) log V)   空间复杂度: O(V + E)
##### ! 适用：最常考的写法；边权 >= 1 保证弹出 u 时所有更近的点都已定案，ways[u] 不会再变
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in roads:
            adj[u].append((v, w))
            adj[v].append((u, w))  # 无向图两边都存

        dist = [inf] * n
        ways = [0] * n  # ! 到每个点的最短路条数
        dist[0], ways[0] = 0, 1
        done = [False] * n
        heap = [(0, 0)]

        while heap:
            d, u = heappop(heap)
            if done[u]:  # 作废票：u 已经定案，它的 ways 已经是最终值
                continue
            done[u] = True
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:  # ! 严格更短：旧记录全部作废，条数直接覆盖
                    dist[v] = nd
                    ways[v] = ways[u]
                    heappush(heap, (nd, v))
                elif nd == dist[v]:  # ! 一样短：条数累加
                    ways[v] = (ways[v] + ways[u]) % MOD

        return ways[n - 1]


##################################################################################################
##### ! Solution 2: 先 Dijkstra 算 dist，再在最短路 DAG 上按 dist 升序 DP 数路径
##### ! 时间复杂度: O((V + E) log V)   空间复杂度: O(V + E)
##### ! 适用：把"算距离"和"数条数"拆成两步，思路更清楚；dist 已知后 DAG 上数路径就是普通拓扑 DP
##################################################################################################


class Solution_2:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in roads:
            adj[u].append((v, w))
            adj[v].append((u, w))

        dist = [inf] * n  # 第一步：743 原样的 Dijkstra
        dist[0] = 0
        heap = [(0, 0)]
        while heap:
            d, u = heappop(heap)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heappush(heap, (d + w, v))

        # 第二步：边 (u, v, w) 在最短路 DAG 上 <=> dist[u] + w == dist[v]
        order = sorted(range(n), key=lambda i: dist[i])  # ! 按 dist 升序就是这张 DAG 的拓扑序 (w >= 1)
        ways = [0] * n
        ways[0] = 1
        for u in order:
            if dist[u] == inf:  # 后面都是到不了的点
                break
            for v, w in adj[u]:
                if dist[u] + w == dist[v]:  # ! 这条边在最短路上，把 u 的条数推给 v
                    ways[v] = (ways[v] + ways[u]) % MOD

        return ways[n - 1]


##################################################################################################
##### ! Solution 3: Floyd 算 dist，再在最短路 DAG 上 DP
##### ! 时间复杂度: O(V^3 + E)   空间复杂度: O(V^2)
##### ! 适用：n <= 200 时 Floyd 也跑得动；只是说明"算 dist 用什么都行，数条数那步不变"
##################################################################################################


class Solution_3:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        d = [[inf] * n for _ in range(n)]
        for i in range(n):
            d[i][i] = 0
        for u, v, w in roads:
            d[u][v] = d[v][u] = min(d[u][v], w)
        for k in range(n):  # Floyd：中转点在最外层
            dk = d[k]
            for i in range(n):
                dik = d[i][k]
                if dik == inf:
                    continue
                di = d[i]
                for j in range(n):
                    if dik + dk[j] < di[j]:
                        di[j] = dik + dk[j]

        dist = d[0]  # 第 0 行就是单源 dist，后面和 Solution 2 第二步一模一样
        adj = [[] for _ in range(n)]
        for u, v, w in roads:
            adj[u].append((v, w))
            adj[v].append((u, w))
        order = sorted(range(n), key=lambda i: dist[i])
        ways = [0] * n
        ways[0] = 1
        for u in order:
            if dist[u] == inf:
                break
            for v, w in adj[u]:
                if dist[u] + w == dist[v]:
                    ways[v] = (ways[v] + ways[u]) % MOD

        return ways[n - 1]


s = Solution_1()
n = 7
roads = [[0, 6, 7], [0, 1, 2], [1, 2, 3], [1, 3, 3], [6, 3, 3], [3, 5, 1], [6, 5, 1], [2, 5, 1], [0, 4, 5], [4, 6, 2]]
result = s.countPaths(n, roads)
print(result)  # 4

n = 2
roads = [[1, 0, 10]]
result = s.countPaths(n, roads)
print(result)  # 1
