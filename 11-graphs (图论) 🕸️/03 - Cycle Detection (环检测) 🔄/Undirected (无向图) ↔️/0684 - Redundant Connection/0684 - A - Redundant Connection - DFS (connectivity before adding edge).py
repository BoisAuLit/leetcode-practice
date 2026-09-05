from collections import defaultdict
from typing import List


class Solution:
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
