from typing import Dict, List

class Solution:
    def dfs(self, graph: Dict[str, List[str]], node: str, visited=None):
        if visited is None:
            visited = set()
        # ! DFS recursive always mark current node as visited in the beginning
        visited.add(node)
        print(node, end=" ")

        for neighbor in graph[node]:
            if neighbor not in visited:
                self.dfs(graph, neighbor, visited)
        

s = Solution()
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
s.dfs(graph, 'A')
