"""LC-1319 - Number of Operations to Make Network Connected

阶段 2 · 并查集 · 计数（块数 = n − 成功合并次数） ○ 核心
题目在问：最少拔插几根网线能把 n 台电脑全连通，线不够就 -1
点是什么：一台电脑   边是什么：一根网线（无向）
和签名题比改了哪一行：323 直接返回块数；本题先判线够不够（len(connections) < n-1 就 -1），
                      然后返回 块数 − 1（把 k 块串起来只要 k−1 根线，多余的线一定够）
"""
from typing import List


class UnionFind:  # 路径减半 + 按 size 合并，union 返回 bool（成功合并才 True）
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
##### ! Solution 1: Union-Find 计数
##### ! 时间复杂度: O((n + E) · α(n))   空间复杂度: O(n)
##### ! 适用：只要块数、不需要遍历结构时最短；就是阶段 2 的标准写法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        if len(connections) < n - 1:  # ! 线不够：连 n 台至少 n−1 根，直接 -1
            return -1
        uf = UnionFind(n)
        blocks = n  # 一开始每台电脑自成一块
        for a, b in connections:
            if uf.union(a, b):  # ! 成功合并一次块数少一；失败说明这根线多余（可以拔）
                blocks -= 1
        return blocks - 1  # ! k 块串成一块要 k−1 根线；线总数 >= n−1 保证多余的线够用


##################################################################################################
##### ! Solution 2: DFS 数连通块
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n + E)
##### ! 适用：静态图数块数的通用写法；要建邻接表，代码比并查集长
##################################################################################################


class Solution_2:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        if len(connections) < n - 1:
            return -1
        adj = [[] for _ in range(n)]
        for a, b in connections:
            adj[a].append(b)
            adj[b].append(a)

        seen = [False] * n
        blocks = 0
        for start in range(n):
            if seen[start]:
                continue
            blocks += 1  # ! 每从一个没见过的点出发一次，就是一块
            seen[start] = True
            stack = [start]  # n 到 1e5，用栈代替递归，避免递归深度超限
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if not seen[v]:
                        seen[v] = True
                        stack.append(v)
        return blocks - 1


s = Solution_1()
n = 4
connections = [[0, 1], [0, 2], [1, 2]]
result = s.makeConnected(n, connections)
print(result)  # 1
print(s.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]))  # 2
print(s.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2]]))  # -1
