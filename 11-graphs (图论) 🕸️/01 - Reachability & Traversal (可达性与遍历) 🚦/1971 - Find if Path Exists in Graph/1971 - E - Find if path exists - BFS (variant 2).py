from typing import List
from collections import deque, defaultdict


"""
Time complexity: O(V+E)
Space complexity: O(V+E)
"""

class Solution:
    def validPath(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        # ! Phase 1: Initialization
        graph = defaultdict(list)
        for x, y in edges:
            graph[x] += (y,)
            graph[y] += (x,)
        queue = deque([source])
        seen = [False] * n
        seen[source] = True

        # ! Phase 2: Iteration
        while queue:
            node = queue.popleft()
            if node == destination:
                return True
            for next_node in graph[node]:
                if not seen[next_node]:
                    seen[next_node] = True
                    queue.append(next_node)

        return False
