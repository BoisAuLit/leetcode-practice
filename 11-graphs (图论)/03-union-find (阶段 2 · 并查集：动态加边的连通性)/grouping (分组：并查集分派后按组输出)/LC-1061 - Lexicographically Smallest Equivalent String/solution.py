"""LC-1061 - Lexicographically Smallest Equivalent String

阶段 2 · 并查集 · 分组（并查集分派后按组输出） ○ 核心
题目在问：s1[i] 和 s2[i] 等价（自反、对称、传递），把 baseStr 每个字母换成它那一派里最小的字母
点是什么：26 个小写字母   边是什么：一对 (s1[i], s2[i])
和签名题比改了哪一行：323 union 完数块数；本题 union 完"每派记最小代表"：
                      从 a 到 z 扫一遍，rep[根] = 这派最小字母，再逐位查表
"""


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
##### ! Solution 1: Union-Find + 每派记最小代表
##### ! 时间复杂度: O((|s1| + |baseStr|) · α(26))   空间复杂度: O(26)
##### ! 适用：模板一个字不改（按 size 合并），union 完多一轮 26 步的"每派取最小"；最通用
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def smallestEquivalentString(self, s1: str, s2: str, baseStr: str) -> str:
        uf = UnionFind(26)
        for a, b in zip(s1, s2):
            uf.union(ord(a) - 97, ord(b) - 97)  # ! 等价就并成一派

        rep = [26] * 26  # rep[根] = 这一派最小的字母编号
        for x in range(26):  # ! 从 a 到 z 扫，每派第一个碰到的就是最小的
            r = uf.find(x)
            rep[r] = min(rep[r], x)

        return "".join(chr(rep[uf.find(ord(ch) - 97)] + 97) for ch in baseStr)


##################################################################################################
##### ! Solution 2: Union-Find，union 时让小字母当根
##### ! 时间复杂度: O((|s1| + |baseStr|) · 26)（不按 size 合并，树可能退化，但点只有 26 个）   空间复杂度: O(26)
##### ! 适用：LeetCode 上最常见的写法；根本身就是答案，省掉"每派取最小"那一轮
##################################################################################################


class Solution_2:
    def smallestEquivalentString(self, s1: str, s2: str, baseStr: str) -> str:
        parent = list(range(26))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in zip(s1, s2):
            ra, rb = find(ord(a) - 97), find(ord(b) - 97)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)  # ! 强制小字母当根，根就是这派的最小字母

        return "".join(chr(find(ord(ch) - 97) + 97) for ch in baseStr)


##################################################################################################
##### ! Solution 3: DFS 分派
##### ! 时间复杂度: O(|s1| + |baseStr| + 26)   空间复杂度: O(|s1| + 26)
##### ! 适用：静态图的等价写法；从 a 到 z 依次起步，每派第一个出发的点就是这派最小字母
##################################################################################################


class Solution_3:
    def smallestEquivalentString(self, s1: str, s2: str, baseStr: str) -> str:
        adj = [[] for _ in range(26)]
        for a, b in zip(s1, s2):
            adj[ord(a) - 97].append(ord(b) - 97)
            adj[ord(b) - 97].append(ord(a) - 97)

        rep = [-1] * 26  # rep[x] = x 那一派的最小字母

        def dfs(u: int, root: int) -> None:  # 只有 26 个点，递归深度不会超限
            rep[u] = root
            for v in adj[u]:
                if rep[v] == -1:
                    dfs(v, root)

        for x in range(26):  # ! 从小到大起步，起点就是这派的最小字母
            if rep[x] == -1:
                dfs(x, x)

        return "".join(chr(rep[ord(ch) - 97] + 97) for ch in baseStr)


s = Solution_1()
s1, s2, baseStr = "parker", "morris", "parser"
result = s.smallestEquivalentString(s1, s2, baseStr)
print(result)  # makkek
print(s.smallestEquivalentString("hello", "world", "hold"))  # hdld
print(s.smallestEquivalentString("leetcode", "programs", "sourcecode"))  # aauaaaaada
