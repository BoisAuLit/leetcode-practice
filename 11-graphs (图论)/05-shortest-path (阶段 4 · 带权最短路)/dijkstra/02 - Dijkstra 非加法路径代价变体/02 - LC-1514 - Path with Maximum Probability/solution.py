"""LC-1514 - Path with Maximum Probability

阶段 4 · Dijkstra 堆版 (relax 写 d + w) ○ 核心题
题目在问：无向图每条边有一个成功概率，从 start_node 走到 end_node 的路径成功概率(沿途概率相乘)最大是多少，到不了返回 0
点是什么：n 个结点   边是什么：edges[i] 配概率 succProb[i]，无向
和签名题比改了哪一行：743 的 relax 是 d + w 取小；这里改成 d * p 取大，堆改成大根堆(概率取负存)，起点标签是 1 不是 0
"""
from collections import deque
from heapq import heappop, heappush
from typing import List

##################################################################################################
##### ! Solution 1: Dijkstra 大根堆 (relax 改成 d * p)
##### ! 时间复杂度: O((V + E) log V)   空间复杂度: O(V + E)
##### ! 适用：单源、概率在 [0, 1] 里，乘一个 p 只会让路径变差，Dijkstra "先弹最好的就定案"的贪心仍然成立
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start_node: int, end_node: int) -> float:
        adj = [[] for _ in range(n)]
        for (u, v), p in zip(edges, succProb):
            adj[u].append((v, p))
            adj[v].append((u, p))  # 无向图两边都存

        best = [0.0] * n  # ! 到每个点的最大概率，初值 0 (743 里是 inf，这里方向反过来)
        best[start_node] = 1.0  # ! 起点概率 1，不是 0
        heap = [(-1.0, start_node)]  # ! (负概率, 点)：heapq 是小根堆，存负数就变成大根堆

        while heap:
            neg, u = heappop(heap)
            p = -neg
            if u == end_node:  # 第一次弹出终点就是最优，可以提前停
                return p
            if p < best[u]:  # 作废票：u 已经用更大的概率处理过
                continue
            for v, w in adj[u]:
                nq = p * w  # ! relax：743 写 d + w，这里写 d * p
                if nq > best[v]:  # ! 比旧记录大才更新
                    best[v] = nq
                    heappush(heap, (-nq, v))

        return 0.0  # 到不了


##################################################################################################
##### ! Solution 2: Bellman-Ford (n - 1 轮，没变化就提前退出)
##### ! 时间复杂度: O(V · E)   空间复杂度: O(V)
##### ! 适用：不想建邻接表、或者边数很少；没有边数限制所以不需要 787 那种快照，原地更新收敛更快
##################################################################################################


class Solution_2:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start_node: int, end_node: int) -> float:
        best = [0.0] * n
        best[start_node] = 1.0

        for _ in range(n - 1):  # ! 最多 n - 1 轮：一条简单路径最多 n - 1 条边
            changed = False
            for (u, v), p in zip(edges, succProb):  # 每轮把所有边松弛一遍，无向所以两个方向都试
                if best[u] * p > best[v]:
                    best[v] = best[u] * p
                    changed = True
                if best[v] * p > best[u]:
                    best[u] = best[v] * p
                    changed = True
            if not changed:  # ! 这一轮谁都没变好，后面也不会变了
                break

        return best[end_node]


##################################################################################################
##### ! Solution 3: SPFA (Bellman-Ford 加队列，只松弛刚变好的点的邻居)
##### ! 时间复杂度: 平均 O(E)，最坏 O(V · E)   空间复杂度: O(V + E)
##### ! 适用：和 Bellman-Ford 同一个思路但跳过没变化的点；随机图上很快，刻意构造的图会退化
##################################################################################################


class Solution_3:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start_node: int, end_node: int) -> float:
        adj = [[] for _ in range(n)]
        for (u, v), p in zip(edges, succProb):
            adj[u].append((v, p))
            adj[v].append((u, p))

        best = [0.0] * n
        best[start_node] = 1.0
        q = deque([start_node])
        in_q = [False] * n  # ! 已经在队列里的点不重复入队
        in_q[start_node] = True

        while q:
            u = q.popleft()
            in_q[u] = False
            for v, w in adj[u]:
                nq = best[u] * w
                if nq > best[v]:  # ! v 变好了，它的邻居才需要重新看
                    best[v] = nq
                    if not in_q[v]:
                        in_q[v] = True
                        q.append(v)

        return best[end_node]


s = Solution_1()
n = 3
edges = [[0, 1], [1, 2], [0, 2]]
succProb = [0.5, 0.5, 0.2]
result = s.maxProbability(n, edges, succProb, 0, 2)
print(result)  # 0.25

succProb = [0.5, 0.5, 0.3]
result = s.maxProbability(n, edges, succProb, 0, 2)
print(result)  # 0.3

edges = [[0, 1]]
succProb = [0.5]
result = s.maxProbability(n, edges, succProb, 0, 2)
print(result)  # 0.0
