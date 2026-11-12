"""LC-0947 - Most Stones Removed with Same Row or Column

阶段 2 · 并查集 · 建模（把别的东西当点） ○ 核心
题目在问：一颗石头的同行或同列还有别的石头就能把它消掉，最多消几颗
点是什么：解法 1 把行号和列号当点（列号 + 10001 和行号错开）；解法 2/3 把石头当点
边是什么：解法 1 一颗石头 = 连它的行和列的一条边；解法 2/3 两颗石头同行或同列
和签名题比改了哪一行：323 数块数的代码一行不改，改的是建模：
                      每块能一直消到只剩 1 颗，所以 答案 = 石头数 − 块数
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
##### ! Solution 1: Union-Find，行号和列号当点
##### ! 时间复杂度: O(n · α(C))，n = 石头数，C = 20002 个行列点   空间复杂度: O(C)
##### ! 适用：把"同行或同列"翻译成"共用一个行点或列点"，n 条边线性扫完；这道题要学的就是这个建模
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def removeStones(self, stones: List[List[int]]) -> int:
        OFFSET = 10001  # 坐标 <= 1e4，列号加 10001 后和行号不会撞
        uf = UnionFind(2 * OFFSET)
        used = set()  # 真正出现过的行点 / 列点，没出现的不算块
        blocks = 0
        for r, c in stones:
            for node in (r, c + OFFSET):
                if node not in used:
                    used.add(node)
                    blocks += 1  # 新出现的行/列点先自成一块
            if uf.union(r, c + OFFSET):  # ! 一颗石头 = 一条边，把它的行和列并成一块
                blocks -= 1
        return len(stones) - blocks  # ! 每块留 1 颗，其余全能消


##################################################################################################
##### ! Solution 2: Union-Find，石头当点，两两比
##### ! 时间复杂度: O(n^2 · α(n))   空间复杂度: O(n)
##### ! 适用：最直白的建模，n <= 1000 能过；答案 = 成功 union 的次数（= 石头数 − 块数）
##################################################################################################


class Solution_2:
    def removeStones(self, stones: List[List[int]]) -> int:
        n = len(stones)
        uf = UnionFind(n)
        removed = 0
        for i in range(n):
            for j in range(i + 1, n):
                if stones[i][0] == stones[j][0] or stones[i][1] == stones[j][1]:  # 同行或同列才连边
                    if uf.union(i, j):  # ! 每成功合并一次块数少一，就多一颗能消
                        removed += 1
        return removed


##################################################################################################
##### ! Solution 3: DFS，石头当点，按行/列表找邻居
##### ! 时间复杂度: O(n)（每个行表/列表只扫一次，扫完就 pop 掉）   空间复杂度: O(n)
##### ! 适用：静态图数块数的 DFS 写法；用 行号 -> 石头表 代替邻接表，省掉两两比较
##################################################################################################


class Solution_3:
    def removeStones(self, stones: List[List[int]]) -> int:
        rows, cols = {}, {}  # 行号 -> 这一行的石头下标；列号同理
        for i, (r, c) in enumerate(stones):
            rows.setdefault(r, []).append(i)
            cols.setdefault(c, []).append(i)

        seen = [False] * len(stones)
        blocks = 0
        for start in range(len(stones)):
            if seen[start]:
                continue
            blocks += 1  # ! 每从一个没见过的石头出发一次，就是一块
            seen[start] = True
            stack = [start]  # 用栈代替递归，n 到 1000 的链会碰到默认递归上限
            while stack:
                i = stack.pop()
                r, c = stones[i]
                for j in rows.pop(r, []) + cols.pop(c, []):  # ! 邻居 = 同行 + 同列；pop 掉这行这列，后面不再重扫
                    if not seen[j]:
                        seen[j] = True
                        stack.append(j)
        return len(stones) - blocks


s = Solution_1()
stones = [[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]
result = s.removeStones(stones)
print(result)  # 5
print(s.removeStones([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]))  # 3
print(s.removeStones([[0, 0]]))  # 0
