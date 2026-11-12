"""LC-0261 - Graph Valid Tree

合并自 3 个解法文件:
  1. 0261 - A - Graph Valid Tree - Union-Find.py
  2. 0261 - B - Graph Valid Tree - DFS (parent tracking).py
  3. 0261 - C - Graph Valid Tree - BFS (parent tracking).py

阶段 2 · 并查集计数 ○ 核心
题目在问：n 个点 + 边列表，能不能构成一棵树（连通 + 无环）
点是什么：0..n-1 的编号   边是什么：edges 里的无向边
和签名题比改了哪一行：和 323 比，先查边数恰好 n−1，再要求没有一次 union 失败（等价于最后只剩 1 派）
"""

from typing import List

from collections import defaultdict

from collections import deque, defaultdict


# ============================================================================
# Solution 1: Union_Find    (原文件: 0261 - A - Graph Valid Tree - Union-Find.py)
# ============================================================================

class UnionFind:
    def __init__(self, n: int):
        self.root = list(range(n))
        self.rank = [1] * n
        self.count = n

    def find(self, x: int) -> int:
        if x == self.root[x]:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootY] > self.rank[rootX]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1
            self.count -= 1

    def getCount(self) -> int:
        return self.count

    def isConnected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

##################################################################################################
##### ! Solution 1: Union-Find（边数 == n−1 + 最后只剩 1 派）
##### ! 时间复杂度: O(n · α(n))   空间复杂度: O(n)
##### ! 适用：边列表直接给、不想建邻接表；边数卡死在 n−1 之后"连通"和"无环"互相等价，只需验一个
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution（手册写法；Solution 4 是同一件事换成看 union 的返回值）
##################################################################################################

class Solution_1_Union_Find:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        uf = UnionFind(n)
        for x, y in edges:
            uf.union(x, y)
        return uf.getCount() == 1

# ============================================================================
# Solution 2: DFS_parent_tracking    (原文件: 0261 - B - Graph Valid Tree - DFS (parent tracking).py)
# ============================================================================

##################################################################################################
##### ! Solution 2: DFS + parent 记录（撞到已访问点就是环，最后还要 len(seen) == n 保证连通）
##### ! 时间复杂度: O(n + E) = O(n)   空间复杂度: O(n)
##### ! 适用：静态图、想顺便验证"从 0 能走遍全图"；递归深度 = 树高，本地跑长链要调 recursionlimit（LeetCode 已调高）
##################################################################################################

class Solution_2_DFS_parent_tracking:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:

        if len(edges) > n - 1:
            return False

        adj = defaultdict(list)

        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        seen = set()

        def acyclic(node, parent):
            if node in seen:
                return False

            seen.add(node)

            for neigh in adj[node]:
                if neigh == parent:
                    continue

                if not acyclic(neigh, node):
                    return False

            return True

        return acyclic(0, -1) and len(seen) == n

# ============================================================================
# Solution 3: BFS_parent_tracking    (原文件: 0261 - C - Graph Valid Tree - BFS (parent tracking).py)
# ============================================================================

##################################################################################################
##### ! Solution 3: BFS + parent 记录（和 Solution 2 同一思路，队列代替递归）
##### ! 时间复杂度: O(n + E) = O(n)   空间复杂度: O(n)
##### ! 适用：同 DFS，但不吃递归深度，n 大时更稳
##################################################################################################

class Solution_3_BFS_parent_tracking:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) > n - 1:
            return False

        adj = defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        seen = set()
        q = deque([(0, -1)])  # (current node, parent node)
        seen.add(0)

        while q:
            node, parent = q.popleft()
            for nei in adj[node]:
                if nei == parent:
                    continue
                if nei in seen:
                    return False
                seen.add(nei)
                q.append((nei, node))

        return len(seen) == n


##################################################################################################
##### ! Solution 4: Union-Find，union 返回 bool（手册原话：恰好 n−1 条边 + 没有一次 union 失败）
##### ! 时间复杂度: O(n · α(n))   空间复杂度: O(n)
##### ! 适用：同 Solution 1；第一次 union 失败就立刻返回，和 684 是同一个动作
##################################################################################################


class UnionFindBool:  # 和 1135 参考文件里的模板一样：路径减半 + 按 size 合并，union 返回 bool
    def __init__(self, n: int):  # 上面用户自己的 UnionFind 名字已占用，所以另起一个名
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # ! 路径减半：每走一步就往上跳一级
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False  # ! 已经同一派，合并失败
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


class Solution_4:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:  # ! 边数不对，直接否
            return False
        uf = UnionFindBool(n)
        return all(uf.union(u, v) for u, v in edges)  # ! 任何一次合并失败 = 成环 = 不是树


s = Solution_1_Union_Find()
n = 5
edges = [[0, 1], [0, 2], [0, 3], [1, 4]]
result = s.validTree(n, edges)
print(result)  # True
result = s.validTree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]])
print(result)  # False
