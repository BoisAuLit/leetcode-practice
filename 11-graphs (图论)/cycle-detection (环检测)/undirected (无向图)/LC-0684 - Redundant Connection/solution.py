"""LC-0684 - Redundant Connection

合并自 2 个解法文件:
  1. 0684 - A - Redundant Connection - DFS (connectivity before adding edge).py
  2. 0684 - B - Redundant Connection - BFS (leaf peeling).py
"""

from typing import List

from collections import defaultdict

from collections import defaultdict, deque


# ============================================================================
# Solution 1: DFS_connectivity_before_adding_edge    (原文件: 0684 - A - Redundant Connection - DFS (connectivity before adding edge).py)
# ============================================================================

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
