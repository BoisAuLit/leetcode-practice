"""LC-0323 - Number of Connected Components in an Undirected Graph

合并自 3 个解法文件:
  1. 0323 - A - Number of Connected Components - Union-Find.py
  2. 0323 - B - Number of Connected Components - DFS.py
  3. 0323 - C - Number of Connected Components - BFS.py
"""

from typing import List

from collections import defaultdict

from collections import deque, defaultdict


# ============================================================================
# Solution 1: Union_Find    (原文件: 0323 - A - Number of Connected Components - Union-Find.py)
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
            elif self.rank[rootX] < self.rank[rootY]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1
            self.count -= 1

    def getCount(self):
        return self.count

    def isConnected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

class Solution_1_Union_Find:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        uf = UnionFind(n)
        for x, y in edges:
            uf.union(x, y)
        return uf.getCount()

# ============================================================================
# Solution 2: DFS    (原文件: 0323 - B - Number of Connected Components - DFS.py)
# ============================================================================

n_2 = 5

edges_2 = [[0, 1], [1, 2], [3, 4]]

class Solution_2_DFS:
    def countComponents(self, n_2: int, edges_2: List[List[int]]) -> int:
        adj = defaultdict(list)

        for a, b in edges_2:
            adj[a].append(b)
            adj[b].append(a)

        nodes = set(range(n_2))  # 所有还没访问过的节点
        res = 0

        while nodes:
            node = nodes.pop()  # 随便选一个未访问节点
            stack = [node]

            while stack:
                node = stack.pop()

                for neigh in adj[node]:
                    if neigh in nodes:
                        nodes.remove(neigh)
                        stack.append(neigh)

            res += 1

        return res

# ============================================================================
# Solution 3: BFS    (原文件: 0323 - C - Number of Connected Components - BFS.py)
# ============================================================================

n_3 = 5

edges_3 = [[0, 1], [1, 2], [3, 4]]

class Solution_3_BFS:
    def countComponents(self, n_3: int, edges_3: List[List[int]]) -> int:
        adj = defaultdict(list)

        for a, b in edges_3:
            adj[a].append(b)
            adj[b].append(a)

        nodes = set(range(n_3))  # 所有还没访问过的节点
        res = 0

        while nodes:  # 随便选一个未访问节点
            node = nodes.pop()
            q = deque([node])

            while q:
                node = q.popleft()

                for neigh in adj[node]:
                    if neigh in nodes:
                        nodes.remove(neigh)
                        q.append(neigh)

            res += 1

        return res


if __name__ == "__main__":

    # --- Solution 2: DFS ---
    s = Solution_2_DFS()
    result = s.countComponents(n_2, edges_2)
    print(result)

    # --- Solution 3: BFS ---
    s = Solution_3_BFS()
    result = s.countComponents(n_3, edges_3)
    print(result)
