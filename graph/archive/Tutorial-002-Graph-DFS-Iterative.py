from typing import Dict, List

class Solution:
    def dfs_recursive(self, graph: Dict[str, List[str]], start: str, visited=None):
        visited = set()
        stack = [start]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                print(node, end=" ")  # or collect in a list
                # Add neighbors in reverse to maintain left-to-right order
                stack.extend(reversed(graph[node]))
            

s = Solution()
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
s.dfs_recursive(graph, 'A')
