"""LC-0684 - Redundant Connection

合并自 2 个解法文件:
  1. 0684 - A - Redundant Connection - DFS (connectivity before adding edge).py
  2. 0684 - B - Redundant Connection - BFS (leaf peeling).py

阶段 2 · 并查集成环 ★ 签名题
题目在问：一棵树多加了一条边，把这条多余的边找出来（多解时取输入里最后出现的）
点是什么：1..n 的编号   边是什么：edges 里的无向边，按输入顺序一条条加
和签名题比改了哪一行：本题就是签名题（按顺序 union，第一次返回 False 的那条边就是答案）
"""

from typing import List

from collections import defaultdict

from collections import defaultdict, deque


# ============================================================================
# Solution 1: DFS_connectivity_before_adding_edge    (原文件: 0684 - A - Redundant Connection - DFS (connectivity before adding edge).py)
# ============================================================================

##################################################################################################
##### ! Solution 1: DFS，加每条边之前先问"两端已经连通了吗"
##### ! 时间复杂度: O(n²)（每条边做一次 O(n) 的 DFS）   空间复杂度: O(n)
##### ! 适用：n 小（本题 n ≤ 1000 能过）、想用最直观的画面理解"动态加边"；并查集就是把这个 O(n) 的连通查询压成 α(n)
##################################################################################################

class Solution_1_DFS_connectivity_before_adding_edge:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        adj = defaultdict(list)

        def connected(start, target):
            stack = [start]
            seen = {start}

            while stack:
                node = stack.pop()

                if node == target:
                    return True

                for neigh in adj[node]:
                    if neigh not in seen:
                        seen.add(neigh)
                        stack.append(neigh)

            return False

        for a, b in edges:
            # 如果 a 和 b 本来已经连通，
            # 再加入 [a, b] 就一定产生 cycle
            if connected(a, b):
                return [a, b]

            # 还不连通，这条边安全，加入 graph
            adj[a].append(b)
            adj[b].append(a)

        return []

# ============================================================================
# Solution 2: BFS_leaf_peeling    (原文件: 0684 - B - Redundant Connection - BFS (leaf peeling).py)
# ============================================================================

##################################################################################################
##### ! Solution 2: BFS 剥叶子（度为 1 的点不可能在环上，剥光后剩下的全是环）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：想拿到整条环（不止一条边）、或图是静态给全的；本质是无向图版的拓扑排序
##################################################################################################

class Solution_2_BFS_leaf_peeling:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)

        adj = defaultdict(list)
        degree = [0] * (n + 1)

        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
            degree[a] += 1
            degree[b] += 1

        q = deque()

        # 所有 leaf 都不可能属于 cycle
        for node in range(1, n + 1):
            if degree[node] == 1:
                q.append(node)

        # 一层一层剥掉 leaves
        while q:
            node = q.popleft()

            degree[node] = 0  # 代表这个 node 已经被删除

            for neigh in adj[node]:
                if degree[neigh] == 0:
                    continue

                degree[neigh] -= 1 

                if degree[neigh] == 1:
                    q.append(neigh)

        # degree > 0 的节点现在全部在 cycle 中
        # 从后往前找最后出现的 cycle edge
        for a, b in reversed(edges):
            if degree[a] > 0 and degree[b] > 0:
                return [a, b]

        return []


##################################################################################################
##### ! Solution 3: Union-Find（按输入顺序 union，第一次返回 False 的那条边就是答案）
##### ! 时间复杂度: O(n · α(n))   空间复杂度: O(n)
##### ! 适用：动态加边问"这条边加上去会不会成环"的标准答案；失败的那条一定是环上最后出现的，天然满足"取最后"
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class UnionFind:  # 和 1135 参考文件里的模板一样：路径减半 + 按 size 合并，union 返回 bool
    def __init__(self, n: int):
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


class Solution_3:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        uf = UnionFind(len(edges) + 1)  # 多开一格：下标 0 闲置，点 1..n 直接用
        for a, b in edges:
            if not uf.union(a, b):  # ! 两端已经同一派，这条边一加就成环
                return [a, b]
        return []


s = Solution_3()
edges = [[1, 2], [1, 3], [2, 3]]
result = s.findRedundantConnection(edges)
print(result)  # [2, 3]
result = s.findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]])
print(result)  # [1, 4]
