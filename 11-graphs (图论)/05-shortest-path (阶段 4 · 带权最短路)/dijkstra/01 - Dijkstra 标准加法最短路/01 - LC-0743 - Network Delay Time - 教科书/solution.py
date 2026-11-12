from typing import List
from collections import defaultdict
import heapq


##################################################################################################
##### ! Solution 1: Dijkstra 堆版 (relax 写 d + w)
##### ! 时间复杂度: O(E log E)   空间复杂度: O(N + E)   堆里最多 E 张票，每张 log
##### ! 适用：非负权单源最短路的默认选择；本题答案取 dist 最大值(最后一个被确定的点)
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1_Dijkstra:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # ! 第一步就是创建 graph
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((w, v))

        visited = 0

        # ! 具体是从 0 开始, 还是从 1 开始, 真的很重要
        # !     倘若是从 0 开始, 那就是 * n --> 因为 index 正好和 node 编号重合
        # !     倘若是从 1 开始, 那就是 * (n+1) --> 因为第一个编号 0 需要被摒弃
        dist = [float("inf")] * (n + 1)

        # ! 由于是从 k 开始, 所以从 k 到 k 的最短距离必然为 0
        dist[k] = 0

        # ! 
        heap = [(0, k)]

        while heap:
            # ! 当一个 node 第一次被剔除的时候，其 cost 必然是最短路径
            # ! 同一个 node 可能多次被剔除，当且仅当其第一次被剔除的时候可算出最短路径，之后被剔除的时候都可以忽略
            cost, node = heapq.heappop(heap)

            # ! Optimizatoin 1
            if dist[node] < cost:
                continue

            visited += 1
            if visited == n:
                return cost

            for weight, neigh in graph[node]:
                new_cost = cost + weight
                if new_cost < dist[neigh]:  # ! Optimization 2
                    dist[neigh] = new_cost
                    heapq.heappush(heap, (new_cost, neigh))
        return -1


##################################################################################################
##### ! Solution 2: Bellman-Ford 快照版 (和 787 一个模板，这里不限边数所以跑满 n-1 轮)
##### ! 时间复杂度: O(N · E)   空间复杂度: O(N)
##### ! 适用：有负权边、或要限制边数时
##################################################################################################


class Solution_2:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        dist = [float("inf")] * (n + 1)
        dist[k] = 0

        # Bellman-Ford: 最多进行 n-1 轮 Relaxation
        for _ in range(n - 1):
            updated = False

            for u, v, w in times:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True

            # 如果本轮没有更新，说明已经收敛
            if not updated:
                break

        ans = max(dist[1:])
        return -1 if ans == float("inf") else ans
