"""LC-3123 - Find Edges in Shortest Paths

Level 1 · 03 最短路计数与结果组合 —— 正反各跑一次 Dijkstra
题目在问：无向带权图，判断每条边是否落在 0 -> n-1 的"某一条"最短路上（不是所有，是存在一条）
点是什么：节点   边是什么：无向边，权 = 距离
和签名题 743 比改了哪一行：模板一行没改，跑两次：
      d0 = 从 0 出发的最短距离，d1 = 从 n-1 出发的最短距离（无向图所以反图就是原图）
      边 (u, v, w) 在某条最短路上  <=>  d0[u] + w + d1[v] == D  或  d0[v] + w + d1[u] == D
      这个"拆成前半段 + 这条边 + 后半段"的套路，和 2203 的反图、1976 的计数是同一类加工

坑：
  - 终点不可达（D == inf）时答案全 false，而且 inf + w + inf 会炸出 nan/溢出，必须先判掉
  - 两个方向都要试：无向边可以正着用也可以反着用
  - 有重边和自环，所以要按"边的下标"输出，不能按 (u, v) 查表
"""

from heapq import heappop, heappush
from typing import List


def dijkstra(n: int, adj: List[List[tuple]], src: int) -> List[float]:
    """标准堆版 Dijkstra，和 743 一字不差。adj[u] = [(v, w, edge_id), ...]"""
    dist = [float("inf")] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heappop(heap)
        if d > dist[u]:
            continue
        for v, w, _ in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heappush(heap, (d + w, v))
    return dist


def build(n: int, edges: List[List[int]]) -> List[List[tuple]]:
    adj = [[] for _ in range(n)]
    for i, (u, v, w) in enumerate(edges):
        adj[u].append((v, w, i))
        adj[v].append((u, w, i))
    return adj


##################################################################################################
##### ! Solution 1: 正反两次 Dijkstra，再逐条边判等
##### ! 时间复杂度: O(E log V)   空间复杂度: O(V + E)
##### ! 适用：所有"这条边/这个点在不在最短路上"的题；两次最短路 + 一次 O(E) 扫描，无状态无递归
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findAnswer(self, n: int, edges: List[List[int]]) -> List[bool]:
        adj = build(n, edges)
        d0 = dijkstra(n, adj, 0)
        d1 = dijkstra(n, adj, n - 1)
        D = d0[n - 1]
        if D == float("inf"):  # ! 先判掉不可达，否则下面的加法全是 inf
            return [False] * len(edges)
        return [d0[u] + w + d1[v] == D or d0[v] + w + d1[u] == D for u, v, w in edges]


##################################################################################################
##### ! Solution 2: 一次 Dijkstra + 从终点沿 tight 边反向 BFS
##### ! 时间复杂度: O(E log V)   空间复杂度: O(V + E)
##### ! 适用：只想跑一次最短路时用；"最短路 DAG"的通用写法，1976 的计数也可以挂在这张 DAG 上
##################################################################################################


class Solution_2:
    def findAnswer(self, n: int, edges: List[List[int]]) -> List[bool]:
        adj = build(n, edges)
        d0 = dijkstra(n, adj, 0)
        ans = [False] * len(edges)
        if d0[n - 1] == float("inf"):
            return ans
        # ! 从终点往回走：只走满足 d0[u] + w == d0[v] 的边（tight 边 = 最短路 DAG 的边）
        seen = [False] * n
        seen[n - 1] = True
        stack = [n - 1]
        while stack:
            v = stack.pop()
            for u, w, eid in adj[v]:
                if d0[u] + w == d0[v]:
                    ans[eid] = True
                    if not seen[u]:
                        seen[u] = True
                        stack.append(u)
        return ans


if __name__ == "__main__":
    cases = [
        (6, [[0, 1, 4], [0, 2, 1], [1, 3, 2], [1, 4, 3], [1, 5, 1], [2, 3, 1], [3, 5, 3], [4, 5, 2]],
         [True, True, True, False, True, True, True, False]),
        (4, [[2, 0, 1], [0, 1, 1], [0, 3, 4], [3, 2, 2]], [True, False, False, True]),
        (2, [[0, 1, 5], [0, 1, 7]], [True, False]),   # 重边：只有便宜的那条算
        (3, [[0, 1, 1]], [False]),                    # 终点不可达 → 全 false
    ]
    for sol in (Solution_1(), Solution_2()):
        for n, edges, want in cases:
            got = sol.findAnswer(n, [e[:] for e in edges])
            assert got == want, f"{type(sol).__name__} n={n}: got {got}, want {want}"
    print("2 个解法全过")
