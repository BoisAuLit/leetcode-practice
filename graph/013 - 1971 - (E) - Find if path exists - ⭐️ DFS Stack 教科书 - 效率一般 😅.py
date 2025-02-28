from typing import List
from collections import deque, defaultdict

"""
Time: O(n+m)
Space: O(n+m)
"""


class Solution:
    def validPath(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        stack = deque([source])
        seen = [False] * n
        seen[source] = True
        graph = defaultdict(list)
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        while stack:
            node = stack.pop()
            if node == destination:
                return True
            for next_node in graph[node]:
                if not seen[next_node]:
                    seen[next_node] = True
                    stack.append(next_node)

        return False


s = Solution()

# Test case 1: Expecting True
n = 3
edges = [[0, 1], [1, 2], [2, 0]]
source = 0
destination = 2

# Test case 2: Expecting False
# n = 6
# edges = [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]]
# source = 0
# destination = 5

# Test case 3: Expecting True
# n = 6
# edges = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [3, 4], [3, 5], [4, 5]]
# source = 0
# destination = 5

result = s.validPath(n, edges, source, destination)
print(result)
