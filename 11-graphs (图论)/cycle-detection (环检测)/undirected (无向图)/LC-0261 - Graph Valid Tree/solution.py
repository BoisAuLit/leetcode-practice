"""LC-0261 - Graph Valid Tree

合并自 3 个解法文件:
  1. 0261 - A - Graph Valid Tree - Union-Find.py
  2. 0261 - B - Graph Valid Tree - DFS (parent tracking).py
  3. 0261 - C - Graph Valid Tree - BFS (parent tracking).py
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
