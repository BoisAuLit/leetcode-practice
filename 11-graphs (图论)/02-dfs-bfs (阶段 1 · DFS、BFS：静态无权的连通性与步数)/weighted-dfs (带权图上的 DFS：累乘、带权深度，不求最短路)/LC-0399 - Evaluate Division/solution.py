"""LC-0399 - Evaluate Division

合并自 2 个解法文件:
  1. 004 - 0399 - Evaluate Division.py
  2. 0399 - A - Evaluate Division - DFS with running product (weighted Union-Find version in archive).py

阶段 1 · 带权图上的 DFS（累乘、带权深度，不求最短路） ○ 核心题
题目在问：给一堆 a / b = v 的等式，回答 c / d 等于多少；变量没出现过或者两边不连通就 -1.0
点是什么：一个变量名   边是什么：a -> b 权 v，同时 b -> a 权 1 / v（双向，权互为倒数）
和签名题比改了哪一行：200 的 DFS 只问"能不能到"；本题 DFS 一路把边权乘起来，到达 target 时手里的乘积就是答案。
    不需要最短路：等式自洽，任何一条路乘出来都一样，找到一条就 return。
    边界：a / a 且 a 在图里 -> 1.0；x / x 且 x 不在图里 -> -1.0，所以先过"在不在图里"这一关再搜
"""

from typing import List, Tuple

from collections import defaultdict
from collections import deque  # Solution_3 的 BFS 用


# ============================================================================
# Solution 1: Evaluate_Division    (原文件: 004 - 0399 - Evaluate Division.py)
# ============================================================================

equations = [
    ["x1", "x2"],
    ["x3", "x4"],
    ["x2", "x4"],
    ["x10", "x20"],
    ["x30", "x40"],
    ["x20", "x40"],
    ["x4", "x40"],
]

values = [2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 19.0]

queries = [["x1", "x10"]]

##################################################################################################
##### ! Solution 1: 带权并查集，root[i] = [父节点, 父节点值 / 自己的值]，find 时沿途把比值乘到根
##### ! 时间复杂度: O((E + Q) · α(V))  建图 E 次 union、Q 次 query   空间复杂度: O(V)
##### ! 适用：等式多、查询多、或等式在线一条条来的时候；每条等式只处理一次，查询近似 O(1)
##### ! 下面 query 里 "len(groups[x]) == 1 and x == y" 那一行见 ⚠️ 注释
##################################################################################################


class UnionFind:
    def __init__(self):
        self.root = []
        self.rank = []
        self.mapping = {}
        self.groups = {}

    def getHash(self, x: str) -> int:
        return self.mapping[x]

    def addIfNeeded(self, x: str) -> int:
        if x not in self.mapping:
            length = len(self.root)
            self.mapping[x] = length
            self.root.append([length, 1])
            self.rank.append(1)

    def find(self, x: int) -> Tuple[int, int]:
        if self.root[x][0] == x:
            return self.root[x]
        parent, ratio = self.root[x]
        self.root[x][0] = self.find(parent)[0]
        self.root[x][1] = self.root[parent][1] * ratio
        return self.root[x]

    def union(self, x: str, y: str, ratio: float) -> None:
        self.addIfNeeded(x)
        self.addIfNeeded(y)

        rootX = self.find(self.getHash(x))[0]
        rootY = self.find(self.getHash(y))[0]

        x_ratio = self.root[self.getHash(x)][1]
        y_ratio = self.root[self.getHash(y)][1]

        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                new_ratio = x_ratio / y_ratio * ratio
                self.root[rootY] = [rootX, new_ratio]
            elif self.rank[rootX] < self.rank[rootY]:
                new_ratio = y_ratio / x_ratio / ratio
                self.root[rootX] = [rootY, new_ratio]
            else:
                new_ratio = x_ratio / y_ratio * ratio
                self.root[rootY] = [rootX, new_ratio]
                self.rank[rootX] += 1

    def connected(self, x: str, y: str) -> bool:
        return self.find(self.getHash(x))[0] == self.find(self.getHash(y))[0]

    def calculate_groups(self) -> None:
        # Expand all trees to the topmost node and update ratios accordingly
        for i in range(len(self.root)):
            self.find(i)
        self.groups = defaultdict(list)
        for index, [root, _] in enumerate(self.root):
            self.groups[root].append(index)

    def query(self, x: str, y: str) -> int:
        if x not in self.mapping or y not in self.mapping:
            return -1
        if not self.connected(x, y):
            return -1
        hashX = self.getHash(x)
        hashY = self.getHash(y)
        # ! ⚠️ 这里有问题（边界）：如果 a 只在 a / a 这种等式里出现过，它的组只有它自己，
        # !    query(a, a) 会返回 -1，但 a 在图里，题意应该是 1.0；Solution 2 / 3 返回 1.0。LeetCode 常规用例碰不到
        if len(self.groups[hashX]) == 1 and hashX == hashY:
            return -1
        return self.find(self.getHash(y))[1] / self.find(self.getHash(x))[1]

class Solution_1_Evaluate_Division:
    def calcEquation(
        self,
        equations: List[List[str]],
        values: List[float],
        queries: List[List[str]],
    ) -> List[float]:
        unionFind = UnionFind()
        for i in range(len(equations)):
            x, y = equations[i]
            ratio = values[i]
            unionFind.union(x, y, ratio)
            # print(f"Mapping: {unionFind.mapping}")
            # print(f"Root: {unionFind.root}")
            # print(f"Rank: {unionFind.rank}")
            # print("----------------------------------------------")
        unionFind.calculate_groups()
        return [unionFind.query(x, y) for x, y in queries]

# ============================================================================
# Solution 2: DFS_with_running_product_weighted_Union_    (原文件: 0399 - A - Evaluate Division - DFS with running product (weighted Union-Find version in archive).py)
# ============================================================================

# The description of the algorithm:
#  we are asked to check if there exists a path between them.
#  If so, we should return the cumulative products along the path as the result.
#
# Dividend: 被除数
# Divisor: 除数
# Quotient: 商
# Remainder: 余数
# 17÷3=5...2

##################################################################################################
##### ! Solution 2: DFS 累乘路径权重（带 seen 的回溯）
##### ! 时间复杂度: O(Q · (V + E))  每个查询最坏走遍整张图   空间复杂度: O(V + E)  邻接表 + 递归栈
##### ! 适用：本文件夹的模板，手册点名的写法；等式 ≤ 20、查询 ≤ 20，怎么写都不慢，选最好讲的
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2_DFS_with_running_product_weighted_Union_:
    def calcEquation(
        self,
        equations: List[List[str]],
        values: List[float],
        queries: List[List[str]],
    ) -> List[float]:
        graph = defaultdict(dict)
        res = []

        for (a, b), val in zip(equations, values):
            graph[a][b] = val
            graph[b][a] = 1 / val

        for a, b in queries:
            res.append(self.backtrack(graph, a, b, 1, set()))

        return res

    def backtrack(self, graph, cur, target, prod, seen):
        if cur not in graph or cur in seen:
            return -1.0

        if cur == target:
            return prod

        seen.add(cur)
        for neighbor, val in graph[cur].items():
            result = self.backtrack(graph, neighbor, target, prod * val, seen)
            if result != -1.0:
                return result

        return -1.0


##################################################################################################
##### ! Solution 3: BFS 累乘路径权重，队列里带 (节点, 从起点到它的乘积)
##### ! 时间复杂度: O(Q · (V + E))   空间复杂度: O(V + E)  邻接表 + 队列
##### ! 适用：和 DFS 一样的思路，换成队列就没有递归；想顺便看"先到的路"长什么样时用它
##################################################################################################


class Solution_3:
    def calcEquation(
        self,
        equations: List[List[str]],
        values: List[float],
        queries: List[List[str]],
    ) -> List[float]:
        graph = defaultdict(dict)
        for (a, b), v in zip(equations, values):
            graph[a][b] = v  # ! a -> b 权 v
            graph[b][a] = 1.0 / v  # ! b -> a 权 1 / v

        def bfs(src: str, dst: str) -> float:
            if src not in graph or dst not in graph:
                return -1.0  # ! 没见过的变量；src == dst 且在图里会在下面第一轮直接返回 1.0
            q = deque([(src, 1.0)])
            seen = {src}
            while q:
                node, prod = q.popleft()
                if node == dst:
                    return prod
                for nxt, w in graph[node].items():
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append((nxt, prod * w))  # ! 乘积跟着格子走
            return -1.0

        return [bfs(a, b) for a, b in queries]


if __name__ == "__main__":

    # --- Solution 1: Evaluate_Division ---
    s = Solution_1_Evaluate_Division()
    result = s.calcEquation(equations, values, queries)
    print(result)

    # --- Solution 2 (Preferred): LeetCode 示例 1 ---
    s = Solution_2_DFS_with_running_product_weighted_Union_()
    result = s.calcEquation(
        [["a", "b"], ["b", "c"]],
        [2.0, 3.0],
        [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]],
    )
    print(result)  # [6.0, 0.5, -1.0, 1, -1.0]   a / a 返回的是起始乘积 1（int），LeetCode 按数值比，1 == 1.0
