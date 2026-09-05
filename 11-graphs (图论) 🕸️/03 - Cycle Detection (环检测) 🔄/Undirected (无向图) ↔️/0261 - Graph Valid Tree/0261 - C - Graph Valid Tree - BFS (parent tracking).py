from typing import List
from collections import deque, defaultdict

class Solution:
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
