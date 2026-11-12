"""LC-0787 - Cheapest Flights Within K Stops

Level 1 · 05 状态扩展与时间约束 —— dist[node] 不够用了，要 dist[node][用了几条边]
题目在问：最多经停 k 站（= 最多坐 k+1 班飞机），从 src 到 dst 最便宜多少
点是什么：机场   边是什么：航班，权 = 票价（有向）
和签名题 743 比改了哪一行：743 的 dist[node] 在这题是错的 ——
      "到 u 最便宜"的那条路可能已经用光了航段数，而一条更贵但用边更少的路才能走到终点。
      所以状态要从 node 扩成 (node, edges_used)，这是本层的核心：标准 dist 不够就加一维

坑：
  - k 是"经停站数"，航段数是 k+1，差一个 1 是本题最常见的错
  - 不能用普通 visited：同一个点要允许以"更贵但用边更少"的身份再来一次
  - Bellman-Ford 必须用上一轮的快照 dist，直接在原数组上松弛会一轮用掉好几条边
  - 图里可能有环（示例 1 就有 0->1->2->0），所以"走更多边"不一定更便宜也不一定更贵
"""

from collections import deque
from heapq import heappop, heappush
from typing import List


##################################################################################################
##### ! Solution 1: Dijkstra + 状态扩展，状态 = (cost, node, edges_used)
##### ! 时间复杂度: O(E * k log(E * k))   空间复杂度: O(V + E)
##### ! 适用：本层的模板题 —— 约束让 dist[node] 失效时，把约束加进状态里，其余和 743 一样
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in flights:
            adj[u].append((v, w))

        # ! best[u] = 已经弹出过的、到 u 的最少航段数。因为按 cost 升序弹，
        # ! 后来的票一定更贵，只有"用的边更少"才值得再扩展一次
        best = [n + 1] * n
        heap = [(0, src, 0)]  # (总票价, 机场, 已用航段数)
        while heap:
            cost, u, used = heappop(heap)
            if u == dst:
                return cost  # ! 第一次弹到终点就是答案
            if used > k or used >= best[u]:
                continue  # ! 航段用超了，或者这张票被"更便宜且边更少"的记录支配了
            best[u] = used
            for v, w in adj[u]:
                heappush(heap, (cost + w, v, used + 1))
        return -1


##################################################################################################
##### ! Solution 2: Bellman-Ford，每轮用上一轮的快照松弛
##### ! 时间复杂度: O(k * E)   空间复杂度: O(V)
##### ! 适用：★ 面试首选 —— 更快、代码更短、也更难写错；"限制 k 条边"本来就是 Bellman-Ford 的主场
##### !      第 i 轮结束时 dist[v] = "最多用 i 条边到 v 的最小花费"，轮数天然就是航段数
##################################################################################################


class Solution_2:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        INF = float("inf")
        dist = [INF] * n
        dist[src] = 0
        for _ in range(k + 1):          # ! k 站经停 = 最多 k+1 条边 = 松弛 k+1 轮
            snapshot = dist[:]          # ! 快照是灵魂：本轮只能基于上一轮的结果，否则一轮串起好几条边
            for u, v, w in flights:
                if snapshot[u] + w < dist[v]:
                    dist[v] = snapshot[u] + w
        return -1 if dist[dst] == INF else dist[dst]


##################################################################################################
##### ! Solution 3: BFS 逐层扩展（一层 = 一个航段）
##### ! 时间复杂度: O(k * E)   空间复杂度: O(V)
##### ! 适用：和解法 2 本质相同，只是把"轮"写成了"队列的层"；想不起 Bellman-Ford 时的等价写法
##################################################################################################


class Solution_3:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in flights:
            adj[u].append((v, w))

        INF = float("inf")
        best = [INF] * n            # ! best[v]：目前为止到 v 的最便宜花费（不限航段）
        best[src] = 0
        q = deque([(src, 0)])
        for _ in range(k + 1):      # ! 恰好扩展 k+1 层
            for _ in range(len(q)):
                u, cost = q.popleft()
                for v, w in adj[u]:
                    # ! 只有变便宜了才往下传，否则同一层会炸开成指数个状态
                    if cost + w < best[v]:
                        best[v] = cost + w
                        q.append((v, cost + w))
        return -1 if best[dst] == INF else best[dst]


if __name__ == "__main__":
    cases = [
        (4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1, 700),
        (3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1, 200),
        (3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0, 500),
        (2, [[1, 0, 10]], 0, 1, 5, -1),      # 方向反了，到不了
        (1, [], 0, 0, 0, 0),                 # 起点就是终点
    ]
    for sol in (Solution_1(), Solution_2(), Solution_3()):
        for n, fl, s, d, k, want in cases:
            got = sol.findCheapestPrice(n, [f[:] for f in fl], s, d, k)
            assert got == want, f"{type(sol).__name__} n={n} k={k}: got {got}, want {want}"
    print("3 个解法全过")
