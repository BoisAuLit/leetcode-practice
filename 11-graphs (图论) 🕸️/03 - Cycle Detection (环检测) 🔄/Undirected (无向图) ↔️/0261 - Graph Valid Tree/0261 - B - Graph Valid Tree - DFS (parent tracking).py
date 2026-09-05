from typing import List
from collections import defaultdict

class Solution:
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
