from typing import Optional

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return node
        visited = {}
        stack = [node]
        visited[node] = Node(node.val, [])
        while stack:
            curr = stack.pop()
            for neighbor in curr.neighbors:
                if neighbor not in visited:
                    visited[neighbor] = Node(neighbor.val, [])
                    stack.append(neighbor)
                # This is how we modify the neighbors of the cloned node in iterative approach
                visited[curr].neighbors.append(visited[neighbor])
        return visited[node]
