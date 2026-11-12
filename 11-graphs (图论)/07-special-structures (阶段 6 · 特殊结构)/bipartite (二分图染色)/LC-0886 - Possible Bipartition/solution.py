"""LC-0886 - Possible Bipartition

阶段 6 · 特殊结构 · 二分图染色 ○ 核心
题目在问：n 个人 (编号 1..n), dislikes 列出互相讨厌的对, 能不能分成两组使讨厌的人不在同一组
点是什么：n 个人   边是什么：每条 dislike [a, b] 是一条无向边
和签名题比改了哪一行：785 换个故事: 多了一步"先把 dislikes 建成邻接表" (编号 1..n, 多开一格), 之后二染色一字不改
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
##### ! Solution 1: 建邻接表 + BFS 二染色
##### ! 时间复杂度: O(n + D) (D = len(dislikes))   空间复杂度: O(n + D)
##### ! 适用：二分图判定的默认写法; 和 785 唯一的区别是要自己建图、编号从 1 开始
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
        adj = [[] for _ in range(n + 1)]  # ! 编号 1..n, 多开一格
        for a, b in dislikes:
            adj[a].append(b)
            adj[b].append(a)

        color = [-1] * (n + 1)  # -1 没染, 0 / 1 两组
        for s in range(1, n + 1):  # ! 图可能不连通 (有人谁都不讨厌): 每个没染色的人都要启动一次
            if color[s] != -1:
                continue
            color[s] = 0
            q = deque([s])
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]  # ! 讨厌的人染相反色 (分到另一组)
                        q.append(v)
                    elif color[v] == color[u]:  # ! 讨厌的两人同组 -> 失败
                        return False
        return True


##################################################################################################
##### ! Solution 2: 并查集 (每个人讨厌的所有人并成一派)
##### ! 时间复杂度: O((n + D) · α(n))   空间复杂度: O(n + D)
##### ! 适用：不想写遍历时; "u 讨厌的人必须全在另一组", u 若和自己讨厌的人同派就矛盾
##################################################################################################


class Solution_2:
    def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
        adj = [[] for _ in range(n + 1)]
        for a, b in dislikes:
            adj[a].append(b)
            adj[b].append(a)

        uf = UnionFind(n + 1)
        for u in range(1, n + 1):
            for v in adj[u]:
                if uf.find(u) == uf.find(v):  # ! u 和自己讨厌的人被并到一派 = 矛盾
                    return False
                uf.union(adj[u][0], v)  # ! u 讨厌的所有人必须同组: 全并到第一个那派
        return True


s = Solution_1()
n = 4
dislikes = [[1, 2], [1, 3], [2, 4]]
result = s.possibleBipartition(n, dislikes)
print(result)  # True
