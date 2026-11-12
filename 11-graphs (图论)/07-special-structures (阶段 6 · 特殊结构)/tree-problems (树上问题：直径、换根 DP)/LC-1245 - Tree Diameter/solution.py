"""LC-1245 - Tree Diameter

阶段 6 · 特殊结构 · 树上问题（直径） ○ 核心
题目在问：树上离得最远的两个点之间有几条边（直径）
点是什么：节点 0..n-1，n = len(edges) + 1   边是什么：edges 里的无向边（树，无环）
和签名题比改了哪一行：阶段 6 的树上问题没有单独签名题，本题就是"两次 BFS"的模板：
    任意点出发 BFS 找最远点 a，再从 a 出发 BFS 找最远点 b，dist(a, b) 就是直径
    为什么对：离任意点最远的点一定是某条直径的端点
"""
import sys
from collections import deque
from typing import List

##################################################################################################
##### ! Solution 1: 两次 BFS
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：面试默认写法，最短、无递归；也能顺便拿到直径的两个端点
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def treeDiameter(self, edges: List[List[int]]) -> int:
        n = len(edges) + 1
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        def bfs(src: int) -> tuple:  # ! 返回 (离 src 最远的点, 距离)
            dist = [-1] * n
            dist[src] = 0
            q = deque([src])
            far = src
            while q:
                u = q.popleft()
                if dist[u] > dist[far]:
                    far = u
                for v in adj[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        q.append(v)
            return far, dist[far]

        a, _ = bfs(0)  # ! 第一次：任意点出发，找到直径的一个端点 a
        _, diameter = bfs(a)  # ! 第二次：从 a 出发，最远距离就是直径
        return diameter


##################################################################################################
##### ! Solution 2: 一次 DFS，每个点记"最深的两条子链"
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：树形 DP 的入门形态；直径 = max(top1 + top2)，经过某个点的最长路径 = 它最深两条子链拼起来
##################################################################################################


class Solution_2:
    def treeDiameter(self, edges: List[List[int]]) -> int:
        n = len(edges) + 1
        sys.setrecursionlimit(max(10000, 2 * n))  # ! 链状树递归深度 = n
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        best = 0

        def dfs(u: int, parent: int) -> int:  # ! 返回从 u 往下的最长链长度（边数）
            nonlocal best
            top1 = top2 = 0  # ! u 的孩子里最深的两条链
            for v in adj[u]:
                if v == parent:
                    continue
                depth = dfs(v, u) + 1
                if depth > top1:
                    top1, top2 = depth, top1
                elif depth > top2:
                    top2 = depth
            best = max(best, top1 + top2)  # ! 经过 u 的最长路径
            return top1

        dfs(0, -1)
        return best


##################################################################################################
##### ! Solution 3: 一层层剥叶子（Kahn 式）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：和 310（最小高度树）同一个动作；剥到最后剩 1 个点直径 = 2·层数，剩 2 个点 = 2·层数 + 1
##################################################################################################


class Solution_3:
    def treeDiameter(self, edges: List[List[int]]) -> int:
        n = len(edges) + 1
        adj = [[] for _ in range(n)]
        degree = [0] * n
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
            degree[u] += 1
            degree[v] += 1

        leaves = [u for u in range(n) if degree[u] <= 1]  # ! n = 1 时唯一的点度为 0，也算叶子
        remaining = n
        layers = 0
        while remaining > 2:  # ! 剩 1 或 2 个点就是树的中心，停
            remaining -= len(leaves)
            layers += 1
            new_leaves = []
            for u in leaves:  # ! 剥掉这一圈叶子，邻居度减 1，变成 1 的就是下一圈
                for v in adj[u]:
                    degree[v] -= 1
                    if degree[v] == 1:
                        new_leaves.append(v)
            leaves = new_leaves
        return 2 * layers if remaining == 1 else 2 * layers + 1  # ! 1 个中心：两边各 layers 条边；2 个中心：中间还多 1 条


s = Solution_1()
edges = [[0, 1], [0, 2]]
result = s.treeDiameter(edges)
print(result)  # 2

edges = [[0, 1], [1, 2], [2, 3], [1, 4], [4, 5]]
result = s.treeDiameter(edges)
print(result)  # 4
