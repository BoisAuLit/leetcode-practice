"""LC-1928 - Minimum Cost to Reach Destination in Time

阶段 4 · Dijkstra + 状态扩展 △ 扩展
题目在问：maxTime 分钟内从城市 0 走到 n-1，经过的城市费用总和最少是多少；超时到不了就 -1
点是什么：状态 (城市, 已用时间)   边是什么：无向道路 (x, y, time)，走一条边时间 +time，进一个城市费用 +passingFees
和签名题比改了哪一行：743 的堆里是 (dist, 点)，这里是 (费用, 已用时间, 点)，按费用弹；
dist 数组换成 best_time[点] 做剪枝：到同一个点时间不比记录的更短就不扩展
"""
from heapq import heappop, heappush
from math import inf
from typing import List

##################################################################################################
##### ! Solution 1: Dijkstra on (cost, time, node) with best-time pruning
##### ! 时间复杂度: O(E · maxTime · log) 最坏，实际远小于它   空间复杂度: O(n + E + 堆)
##### ! 适用：两个维度 (费用、时间) 一个要最小化、一个只是上限；按要最小化的维度弹堆，用上限维度剪枝
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        n = len(passingFees)
        adj = [[] for _ in range(n)]
        for u, v, t in edges:
            adj[u].append((v, t))
            adj[v].append((u, t))

        # ! best_time[v]：目前为止到 v 的最短已用时间
        # ! 堆按费用弹，所以后弹出的费用只会更高；到同一个点时间又不更短，就是被支配的状态，直接扔
        best_time = [inf] * n
        best_time[0] = 0
        heap = [(passingFees[0], 0, 0)]  # (费用, 已用时间, 城市)，起点也要交费
        while heap:
            cost, t, u = heappop(heap)
            if u == n - 1:  # ! 第一次弹到终点就是最少费用
                return cost
            for v, w in adj[u]:
                nt = t + w
                if nt > maxTime or nt >= best_time[v]:  # 超时 / 被支配
                    continue
                best_time[v] = nt
                heappush(heap, (cost + passingFees[v], nt, v))
        return -1


##################################################################################################
##### ! Solution 2: DP over time, dp[t][v]
##### ! 时间复杂度: O(maxTime · E)   空间复杂度: O(maxTime · n)
##### ! 适用：时间上限小 (≤ 1000) 时把时间当第二维直接打表；和 787 的"按边数分层"同一个套路，层换成时间
##################################################################################################


class Solution_2:
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        n = len(passingFees)
        # ! dp[t][v]：恰好在时刻 t 站在 v 的最少费用（允许重复经过，费用照收，反正最优解不会绕）
        dp = [[inf] * n for _ in range(maxTime + 1)]
        dp[0][0] = passingFees[0]
        for t in range(1, maxTime + 1):
            cur = dp[t]
            for u, v, w in edges:
                if w > t:
                    continue
                prev = dp[t - w]  # ! 从 t - w 时刻的 u 走这条边，t 时刻到 v
                if prev[u] + passingFees[v] < cur[v]:
                    cur[v] = prev[u] + passingFees[v]
                if prev[v] + passingFees[u] < cur[u]:  # 无向，反方向也要
                    cur[u] = prev[v] + passingFees[u]
        ans = min(dp[t][n - 1] for t in range(maxTime + 1))  # 任意时刻到终点都行
        return -1 if ans == inf else ans


s = Solution_1()
edges = [[0, 1, 10], [1, 2, 10], [2, 5, 10], [0, 3, 1], [3, 4, 10], [4, 5, 15]]
passingFees = [5, 1, 2, 20, 20, 3]
print(s.minCost(30, edges, passingFees))  # 11
print(s.minCost(29, edges, passingFees))  # 48
print(s.minCost(25, edges, passingFees))  # -1
