from typing import List
from collections import defaultdict


class Solution:
    def leadsToDestination(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        g = defaultdict(set)
        visited = defaultdict(int)
        for [x, y] in edges:
            g[x].add(y)

        def dfs(node):
            if visited[node] == 1:
                return True
            elif visited[node] == -1:
                return False
            elif len(g[node]) == 0:
                return node == destination
            else:
                visited[node] = -1
                for child in g[node]:
                    if not dfs(child):
                        return False
                visited[node] = 1
                return True

        return dfs(source)


s = Solution()

# Test case 1: Expecting False
# n = 4
# edges = [[0, 1], [0, 3], [1, 2], [2, 1]]
# source = 0
# destination = 3

# Test case 2: Expecting True
n = 4
edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
source = 0
destination = 3

result = s.leadsToDestination(n, edges, source, destination)
print(result)
