"""LC-0785 - Is Graph Bipartite?

阶段 6 · 特殊结构 · 二分图染色 ★ 签名题
题目在问：无向图能不能把点分成两组, 使每条边的两端都在不同组
点是什么：graph 的下标 u (0..n-1)   边是什么：u 和 graph[u] 里的每个 v (邻接表题目直接给了)
和签名题比改了哪一行：本题就是签名题: BFS / DFS 二染色, 邻居染相反色, 相邻同色就失败; 图可能不连通, 每个没染色的点都要启动一次
"""
from collections import deque
from typing import List


class UnionFind:  # 路径减半 + 按 size 合并, 和 1135 / 1584 一样
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


##################################################################################################
##### ! Solution 1: BFS 二染色
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)
##### ! 适用：二分图判定的默认写法, 不递归, 点再多也不怕
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        color = [-1] * n  # -1 没染, 0 / 1 两种颜色
        for s in range(n):  # ! 图可能不连通: 每个没染色的点都要启动一次
            if color[s] != -1:
                continue
            color[s] = 0
            q = deque([s])
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]  # ! 邻居染成相反色
                        q.append(v)
                    elif color[v] == color[u]:  # ! 相邻同色 -> 不是二分图
                        return False
        return True


##################################################################################################
##### ! Solution 2: DFS 二染色 (递归)
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V) (递归栈最深 V)
##### ! 适用：和 BFS 完全等价, 代码更短; 本题 n <= 100 递归没问题, 点到 1e5 要改迭代或 sys.setrecursionlimit
##################################################################################################


class Solution_2:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        color = [-1] * n

        def dfs(u: int, c: int) -> bool:  # 把 u 染成 c, 顺着边染整个连通块, 撞到同色就 False
            color[u] = c
            for v in graph[u]:
                if color[v] == -1:
                    if not dfs(v, 1 - c):
                        return False
                elif color[v] == c:  # ! 相邻同色
                    return False
            return True

        for s in range(n):
            if color[s] == -1 and not dfs(s, 0):
                return False
        return True


##################################################################################################
##### ! Solution 3: 并查集 (把每个点的所有邻居并成一派)
##### ! 时间复杂度: O((V + E) · α(V))   空间复杂度: O(V)
##### ! 适用：不想写遍历时; 思路是"u 的邻居必须全在另一组", u 自己若和邻居同派就矛盾
##################################################################################################


class Solution_3:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        uf = UnionFind(n)
        for u in range(n):
            for v in graph[u]:
                if uf.find(u) == uf.find(v):  # ! u 和自己的邻居被并到一派 = 矛盾
                    return False
                uf.union(graph[u][0], v)  # ! u 的所有邻居必须同组: 全并到第一个邻居那派
        return True


s = Solution_1()
graph = [[1, 3], [0, 2], [1, 3], [0, 2]]
result = s.isBipartite(graph)
print(result)  # True
