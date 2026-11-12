"""LC-1334 - Find the City With the Smallest Number of Neighbors at a Threshold Distance

Level 1 · 01 标准加法最短路 —— 多次调用标准 Dijkstra
题目在问：每个城市在 distanceThreshold 以内能到几个别的城市；返回邻居最少的那个，并列取编号最大的
点是什么：城市   边是什么：双向道路，权 = 距离（正数）
和签名题 743 比改了哪一行：一行都没改。743 从一个源点跑一次，这题从 n 个源点各跑一次，
      再数 dist[j] <= threshold 的个数 —— 这就是"多源重复调用标准模板"的典型

坑：
  - 并列时要编号最大：循环用 <= 而不是 <（或者从后往前遍历），写成 < 会返回编号最小的那个
  - 数邻居时要排除自己（dist[i][i] = 0 一定 <= threshold）
  - n <= 100 且边稠密，Floyd O(n^3) = 1e6 也完全够；面试里两种都说得出来是加分项
"""

from heapq import heappop, heappush
from typing import List


##################################################################################################
##### ! Solution 1: 对每个点跑一遍标准 Dijkstra
##### ! 时间复杂度: O(n * E log n)   空间复杂度: O(n + E)
##### ! 适用：稀疏图的多源重复查询；模板和 743 一字不差，只是外面套了一层循环
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))  # ! 无向图，两边都加

        def dijkstra(src: int) -> List[float]:
            dist = [float("inf")] * n
            dist[src] = 0
            heap = [(0, src)]
            while heap:
                d, u = heappop(heap)
                if d > dist[u]:  # ! 作废票：这条记录比已知的差，跳过
                    continue
                for v, w in adj[u]:
                    nd = d + w  # ! relax 就是最朴素的 d + w
                    if nd < dist[v]:
                        dist[v] = nd
                        heappush(heap, (nd, v))
            return dist

        best_city, best_cnt = -1, n + 1
        for i in range(n):
            dist = dijkstra(i)
            cnt = sum(1 for j in range(n) if j != i and dist[j] <= distanceThreshold)
            if cnt <= best_cnt:  # ! <= ：编号大的覆盖编号小的，正好满足"并列取最大"
                best_city, best_cnt = i, cnt
        return best_city


##################################################################################################
##### ! Solution 2: Floyd-Warshall 全源最短路
##### ! 时间复杂度: O(n^3)   空间复杂度: O(n^2)
##### ! 适用：★ n <= 100 时代码最短最不容易写错；点少、边稠密、要所有点对时比 n 遍 Dijkstra 更合适
##################################################################################################


class Solution_2:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        INF = float("inf")
        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:
            dist[u][v] = min(dist[u][v], w)  # ! min：题目虽说没有重边，习惯上还是防一手
            dist[v][u] = dist[u][v]

        for k in range(n):          # ! k 必须在最外层：含义是"只允许借 0..k 号点中转"
            dk = dist[k]
            for i in range(n):
                dik = dist[i][k]
                if dik == INF:
                    continue
                row = dist[i]
                for j in range(n):
                    if dik + dk[j] < row[j]:
                        row[j] = dik + dk[j]

        best_city, best_cnt = -1, n + 1
        for i in range(n):
            cnt = sum(1 for j in range(n) if j != i and dist[i][j] <= distanceThreshold)
            if cnt <= best_cnt:
                best_city, best_cnt = i, cnt
        return best_city


##################################################################################################
##### ! Solution 3: Dijkstra + 阈值剪枝（超过 threshold 的点不再往外扩）
##### ! 时间复杂度: O(n * E log n) 最坏不变   空间复杂度: O(n + E)
##### ! 适用：threshold 远小于图直径时实际快很多；思路是"只搜半径 threshold 的球"
##################################################################################################


class Solution_3:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        def count_within(src: int) -> int:
            dist = {src: 0}
            heap = [(0, src)]
            while heap:
                d, u = heappop(heap)
                if d > dist[u]:
                    continue
                for v, w in adj[u]:
                    nd = d + w
                    # ! 剪枝：超过阈值的点对答案没有贡献，连进堆都不用进
                    if nd <= distanceThreshold and nd < dist.get(v, float("inf")):
                        dist[v] = nd
                        heappush(heap, (nd, v))
            return len(dist) - 1  # 减掉自己

        best_city, best_cnt = -1, n + 1
        for i in range(n):
            cnt = count_within(i)
            if cnt <= best_cnt:
                best_city, best_cnt = i, cnt
        return best_city


if __name__ == "__main__":
    cases = [
        (4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4, 3),
        (5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2, 0),
        (2, [[0, 1, 10]], 5, 1),          # 谁也到不了谁 → 并列 0，取编号大的
        (3, [[0, 1, 1], [1, 2, 1]], 100, 2),  # 全连通 → 并列 2，取编号大的
    ]
    for sol in (Solution_1(), Solution_2(), Solution_3()):
        for n, edges, th, want in cases:
            got = sol.findTheCity(n, [e[:] for e in edges], th)
            assert got == want, f"{type(sol).__name__} n={n}: got {got}, want {want}"
    print("3 个解法全过")


##################################################################################################
##### ! Solution Alt: Floyd-Warshall（全源最短路）
##### ! 这是同一道题在本专题**另一个算法家族**里的实现 —— 不同算法，不是重复文件。
##### ! 主学习位置：dijkstra/01 - Dijkstra 标准加法最短路/02 - LC-1334 - Find the City With the Smallest Number of Neighbors at a Threshold Distance
##### ! 变体目录　：floyd (Floyd：所有点对，点 ≤ 100)/变体 · LC-1334 - Find the City With the Smallest Number of Neighbors at a Threshold Distance - ★ 签名题
##### ! 为什么这样定主次：instructions 明确 Floyd 是 P2 参考分类、不作为核心记忆；优先用「对每个点各跑一次 Dijkstra」理解本题
##### ! 为了让复习队列里一道题只出现一次，变体目录已改名为「变体 · …」（不再匹配题目前缀），
#####   但**文件一个都没删**，PDF / metadata / 笔记都还在原处。
##### ! 下面只搬了它的 import 和 class（类名加 _Alt 后缀避免冲突），
#####   原文件底部的示例驱动代码没有搬，以免干扰本文件的测试。
##################################################################################################


from heapq import heappop, heappush


from math import inf


from typing import List


class Solution_1_Alt:
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


class Solution_2_Alt:
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
