from typing import Dict, List
from collections import deque

class Solution:
    def bfs_iterative(self, graph: Dict[str, List[str]], start: str):
        visited = set()
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                print(node, end= " ")
                queue.extend(graph[node])

s = Solution()
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
result = s.bfs_iterative(graph, 'A')

