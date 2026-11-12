"""LC-0990 - Satisfiability of Equality Equations

阶段 2 · 并查集 · 分组（并查集分派后按组输出） ○ 核心
题目在问：一堆 a==b、c!=d 能不能同时成立
点是什么：26 个小写字母   边是什么：一条 == 方程（!= 不是边，是事后要检查的约束）
和签名题比改了哪一行：323 union 完数块数；本题分两轮：第一轮把所有 == 都 union，
                      第二轮逐条看 !=，两端同根就矛盾（x!=x 也会在这里被抓到）
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
##### ! Solution 1: Union-Find 两轮扫描
##### ! 时间复杂度: O(E · α(26))，E = 方程数   空间复杂度: O(26)
##### ! 适用："等价关系 + 若干不等约束"的标准解；先把能并的全并掉，再查矛盾
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def equationsPossible(self, equations: List[str]) -> bool:
        uf = UnionFind(26)
        for eq in equations:  # 方程长得像 "a==b" / "a!=b"，eq[1] 看是哪种
            if eq[1] == "=":  # ! 第一轮：只看 ==，把两边并成一派
                uf.union(ord(eq[0]) - 97, ord(eq[3]) - 97)
        for eq in equations:
            if eq[1] == "!":  # ! 第二轮：!= 的两边不能同根
                if uf.find(ord(eq[0]) - 97) == uf.find(ord(eq[3]) - 97):
                    return False
        return True


##################################################################################################
##### ! Solution 2: DFS 染色分派
##### ! 时间复杂度: O(E + 26)   空间复杂度: O(E + 26)
##### ! 适用：静态图的等价写法；== 建邻接表，DFS 给每个连通块编号，再查 != 两端编号是否相同
##################################################################################################


class Solution_2:
    def equationsPossible(self, equations: List[str]) -> bool:
        adj = [[] for _ in range(26)]
        for eq in equations:
            if eq[1] == "=":
                a, b = ord(eq[0]) - 97, ord(eq[3]) - 97
                adj[a].append(b)
                adj[b].append(a)

        color = [-1] * 26  # color[x] = 字母 x 属于第几派

        def dfs(u: int, c: int) -> None:  # 只有 26 个点，递归深度不会超限
            color[u] = c
            for v in adj[u]:
                if color[v] == -1:
                    dfs(v, c)

        for u in range(26):
            if color[u] == -1:
                dfs(u, u)  # ! 用起点编号当派别号

        return all(
            color[ord(eq[0]) - 97] != color[ord(eq[3]) - 97]  # ! != 两端不能同派
            for eq in equations
            if eq[1] == "!"
        )


s = Solution_1()
equations = ["a==b", "b!=a"]
result = s.equationsPossible(equations)
print(result)  # False
print(s.equationsPossible(["b==a", "a==b"]))  # True
print(s.equationsPossible(["a==b", "b!=c", "c==a"]))  # False
