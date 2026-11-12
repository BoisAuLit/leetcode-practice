"""LC-1786 - Number of Restricted Paths From First to Last Node

Level 1 · 03 最短路计数与结果组合 —— 反向 Dijkstra + 最短路 DAG 上计数
题目在问：点编号 1..n，distanceToLastNode(x) = x 到 n 的最短距离。
      一条「受限路径」要求沿途 dist 严格递减；问 1 到 n 有多少条，答案对 1e9+7 取模
点是什么：节点   边是什么：无向带权边
和签名题 743 比改了哪一行：模板一行没改，但**从 n 出发跑**（不是从 1），得到 dist[]。
      这题把本层另外两道题合在一起：
        - 和 3123 一样，用的是「从终点出发的 dist」（反向最短路）
        - 和 1976 一样，最后要在一张 DAG 上做计数
      关键洞察：条件 dist[u] > dist[v] 天然无环，所以「所有边按 dist 定向」就得到一张 DAG，
      DAG 上的路径计数就是一个简单 DP —— 不需要 visited，也不会数重

坑：
  - 节点是 1-indexed，数组开 n+1；从 n 跑 Dijkstra 而不是从 1
  - 严格递减（>），不是 >=；相等的边不能走，否则会出现环、数到无穷
  - 这里的 DAG 不是「最短路 DAG」：边 (u,v) 只要 dist[u] > dist[v] 就能用，
    不要求 dist[u] == dist[v] + w。写成 tight 边会漏掉一大半答案
  - 全程取模；n 到 2e4、边到 4e4，递归版要手动加大递归上限或者改迭代
"""

from heapq import heappop, heappush
from typing import List

MOD = 10 ** 9 + 7


def dijkstra_from_last(n: int, adj: List[List[tuple]]) -> List[float]:
    """标准堆版 Dijkstra，和 743 一字不差，只是源点取 n。"""
    dist = [float("inf")] * (n + 1)
    dist[n] = 0
    heap = [(0, n)]
    while heap:
        d, u = heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heappush(heap, (d + w, v))
    return dist


def build(n: int, edges: List[List[int]]) -> List[List[tuple]]:
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


##################################################################################################
##### ! Solution 1: 反向 Dijkstra + 按 dist 升序递推计数
##### ! 时间复杂度: O(E log V)   空间复杂度: O(V + E)
##### ! 适用：DAG 计数的标准写法；按 dist 排序就是拓扑序，无递归、无栈溢出风险
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def countRestrictedPaths(self, n: int, edges: List[List[int]]) -> int:
        adj = build(n, edges)
        dist = dijkstra_from_last(n, adj)

        # ! ways[u] = 从 u 出发、沿 dist 严格递减走到 n 的路径数
        ways = [0] * (n + 1)
        ways[n] = 1
        # ! dist 升序就是这张 DAG 的拓扑序：算 u 时，所有 dist 更小的邻居都已经算完
        for u in sorted(range(1, n + 1), key=lambda x: dist[x]):
            if u == n:
                continue
            total = 0
            for v, _ in adj[u]:
                if dist[v] < dist[u]:  # ! 严格递减才算受限路径
                    total += ways[v]
            ways[u] = total % MOD
        return ways[1] % MOD


##################################################################################################
##### ! Solution 2: 反向 Dijkstra + 记忆化 DFS（自顶向下）
##### ! 时间复杂度: O(E log V)   空间复杂度: O(V + E)
##### ! 适用：想法最直接的写法 —— "从 1 出发有几条路" 递归定义；n 大时要防递归深度
##################################################################################################


class Solution_2:
    def countRestrictedPaths(self, n: int, edges: List[List[int]]) -> int:
        adj = build(n, edges)
        dist = dijkstra_from_last(n, adj)
        memo = [-1] * (n + 1)
        memo[n] = 1

        # ! 显式栈的后序遍历：先把所有能走的邻居算完，再回来求和（避免 Python 递归上限）
        stack = [(1, False)]
        while stack:
            u, done = stack.pop()
            if memo[u] != -1:
                continue
            if done:
                memo[u] = sum(memo[v] for v, _ in adj[u] if dist[v] < dist[u]) % MOD
                continue
            stack.append((u, True))
            for v, _ in adj[u]:
                if dist[v] < dist[u] and memo[v] == -1:
                    stack.append((v, False))
        return memo[1] if memo[1] != -1 else 0


##################################################################################################
##### ! Solution 3: 一边跑 Dijkstra 一边计数（弹出即定型，顺手累加）
##### ! 时间复杂度: O(E log V)   空间复杂度: O(V + E)
##### ! 适用：只扫一遍；利用「堆弹出顺序就是 dist 升序」，省掉解法 1 的那次排序
##################################################################################################


class Solution_3:
    def countRestrictedPaths(self, n: int, edges: List[List[int]]) -> int:
        adj = build(n, edges)
        dist = [float("inf")] * (n + 1)
        dist[n] = 0
        ways = [0] * (n + 1)
        ways[n] = 1
        heap = [(0, n)]
        while heap:
            d, u = heappop(heap)
            if d > dist[u]:
                continue
            # ! u 这一刻定型，所有 dist 比它小的点都已经弹过，ways 已是最终值
            if u != n:
                ways[u] = sum(ways[v] for v, _ in adj[u] if dist[v] < dist[u]) % MOD
            if u == 1:
                return ways[1]  # ! 1 号点一定型就能收工
            for v, w in adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heappush(heap, (d + w, v))
        return ways[1] % MOD


if __name__ == "__main__":
    cases = [
        (5, [[1, 2, 3], [1, 3, 3], [2, 3, 1], [1, 4, 2], [5, 2, 2], [3, 5, 1], [5, 4, 10]], 3),
        (7, [[1, 3, 1], [4, 1, 2], [7, 3, 4], [2, 5, 3], [5, 6, 1], [6, 7, 2], [7, 5, 3], [2, 6, 4]], 1),
        (2, [[1, 2, 5]], 1),
        (3, [[1, 2, 1], [2, 3, 1]], 1),
    ]
    for sol in (Solution_1(), Solution_2(), Solution_3()):
        for n, edges, want in cases:
            got = sol.countRestrictedPaths(n, [e[:] for e in edges])
            assert got == want, f"{type(sol).__name__} n={n}: got {got}, want {want}"
    print("3 个解法全过")
