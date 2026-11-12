"""LC-1334 - Find the City With the Smallest Number of Neighbors at a Threshold Distance

阶段 4 · Floyd (所有点对，点 ≤ 100) ★ 签名题
题目在问：每个城市在 distanceThreshold 内能到达几个别的城市，取数量最少的那个（并列取编号最大的）
点是什么：城市 0..n-1   边是什么：无向带权道路 (from, to, weight)
和签名题比改了哪一行：本题就是签名题；k 放最外层，dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
"""
from heapq import heappop, heappush
from math import inf
from typing import List

##################################################################################################
##### ! Solution 1: Floyd-Warshall
##### ! 时间复杂度: O(n^3)   空间复杂度: O(n^2)
##### ! 适用：点数 ≤ 100、要所有点对的最短路；三层循环写完直接查表
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        # ! 画面：一张 n x n 的表，dist[i][j] 是 i 到 j 目前已知的最短距离
        dist = [[inf] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:
            dist[u][v] = min(dist[u][v], w)  # 无向图两边都填，重边取小
            dist[v][u] = min(dist[v][u], w)

        # ! k 必须在最外层：第 k 轮做完，表里是"只允许拿 0..k 当中转"的最短路
        for k in range(n):
            dk = dist[k]
            for i in range(n):
                dik = dist[i][k]
                if dik == inf:  # i 到不了 k，这一行不用看
                    continue
                di = dist[i]
                for j in range(n):
                    if dik + dk[j] < di[j]:
                        di[j] = dik + dk[j]

        best_city, best_cnt = -1, inf
        for i in range(n):
            cnt = sum(1 for j in range(n) if j != i and dist[i][j] <= distanceThreshold)
            if cnt <= best_cnt:  # ! 用 <=，并列时编号大的覆盖编号小的
                best_city, best_cnt = i, cnt
        return best_city


##################################################################################################
##### ! Solution 2: Dijkstra from every node
##### ! 时间复杂度: O(n · E log n)   空间复杂度: O(n + E)
##### ! 适用：点多边少 (稀疏图) 时比 Floyd 快；本题 n ≤ 100 两种都过，Floyd 更短
##################################################################################################


class Solution_2:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        def dijkstra(src: int) -> List[int]:  # 743 的模板原样搬过来
            dist = [inf] * n
            dist[src] = 0
            heap = [(0, src)]
            while heap:
                d, u = heappop(heap)
                if d > dist[u]:  # 作废票
                    continue
                if d > distanceThreshold:  # ! 弹出的已经超阈值，后面的更远，不用再算
                    break
                for v, w in adj[u]:
                    if d + w < dist[v]:
                        dist[v] = d + w
                        heappush(heap, (d + w, v))
            return dist

        best_city, best_cnt = -1, inf
        for i in range(n):  # 每个城市当一次源点
            dist = dijkstra(i)
            cnt = sum(1 for j in range(n) if j != i and dist[j] <= distanceThreshold)
            if cnt <= best_cnt:
                best_city, best_cnt = i, cnt
        return best_city


s = Solution_1()
n = 4
edges = [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]]
distanceThreshold = 4
result = s.findTheCity(n, edges, distanceThreshold)
print(result)  # 3

n = 5
edges = [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]]
distanceThreshold = 2
result = s.findTheCity(n, edges, distanceThreshold)
print(result)  # 0
