"""LC-2203 - Minimum Weighted Subgraph With the Required Paths

阶段 4 · Dijkstra + 状态扩展 △ 扩展
题目在问：有向带权图里挑一个边权和最小的子图，让 src1 和 src2 都能到 dest；做不到返回 -1
点是什么：0..n-1   边是什么：有向边 (from, to, weight)
和签名题比改了哪一行：743 跑一次 Dijkstra 取 dist 最大值；这里同一个 dijkstra 函数跑三次（正图 src1、正图 src2、反图 dest），
答案不是某个 dist，而是枚举汇合点 x 取 d1[x] + d2[x] + d3[x] 的最小值
"""
from heapq import heappop, heappush
from math import inf
from typing import List

##################################################################################################
##### ! Solution 1: Dijkstra three times (src1, src2 on the graph, dest on the reversed graph) + enumerate the meeting node
##### ! 时间复杂度: O(3 · E log n + n) = O(E log n)   空间复杂度: O(n + E)
##### ! 适用：两个源一个汇、要"子图总权"而不是"路径长度"的题；只有这一种标准解法，
##### ! 换成 Bellman-Ford / SPFA 也只是把三次最短路换个算法，形状不变
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minimumWeight(self, n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
        # ! 为什么答案长这样：子图里取一条 src1 -> dest 的路 P1 和一条 src2 -> dest 的路 P2，
        # ! 设 x 是 P1 上第一个也在 P2 上的点（最晚就是 dest 本身）；
        # ! 那么 P1 的 src1 -> x 段、P2 的 src2 -> x 段、P2 的 x -> dest 段两两不共边，
        # ! 所以子图总权 >= d1[x] + d2[x] + d3[x]；反过来三条最短路的并就是一个合法子图。
        # ! 画面：两条路先各自走到汇合点 x，再手拉手一起走到 dest，共用的那段只算一次钱
        adj = [[] for _ in range(n)]
        radj = [[] for _ in range(n)]  # 反图：边反向，"从 dest 出发能到谁"就是"谁能到 dest"
        for u, v, w in edges:
            adj[u].append((v, w))
            radj[v].append((u, w))

        def dijkstra(graph: List[List[tuple]], src: int) -> List[int]:  # 743 的模板，图当参数传
            dist = [inf] * n
            dist[src] = 0
            heap = [(0, src)]
            while heap:
                d, u = heappop(heap)
                if d > dist[u]:  # 作废票
                    continue
                for v, w in graph[u]:
                    if d + w < dist[v]:
                        dist[v] = d + w
                        heappush(heap, (d + w, v))
            return dist

        d1 = dijkstra(adj, src1)  # src1 到每个点
        d2 = dijkstra(adj, src2)  # src2 到每个点
        d3 = dijkstra(radj, dest)  # ! 每个点到 dest（在反图上从 dest 出发）
        ans = min(d1[x] + d2[x] + d3[x] for x in range(n))  # ! 枚举汇合点 x
        return -1 if ans == inf else ans


s = Solution_1()
n = 6
edges = [[0, 2, 2], [0, 5, 6], [1, 0, 3], [1, 4, 5], [2, 1, 1], [2, 3, 3], [2, 3, 4], [3, 4, 2], [4, 5, 1]]
result = s.minimumWeight(n, edges, src1=0, src2=1, dest=5)
print(result)  # 9

n = 3
edges = [[0, 1, 1], [2, 1, 1]]
result = s.minimumWeight(n, edges, src1=0, src2=1, dest=2)
print(result)  # -1
