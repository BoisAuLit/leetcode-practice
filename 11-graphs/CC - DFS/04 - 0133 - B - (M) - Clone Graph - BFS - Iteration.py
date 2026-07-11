from collections import deque

"""
# Definition for a Node.
"""


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: "Node") -> "Node":
        if not node:
            return node

        queue = deque([node])
        visited = {node.val: Node(node.val, [])}
        while queue:
            curr = queue.popleft()
            curr_clone = visited[curr.val]

            for neighbor in curr.neighbors:
                if neighbor.val not in visited:
                    visited[neighbor.val] = Node(neighbor.val, [])
                    queue.append(neighbor)

                curr_clone.neighbors.append(visited[neighbor.val])

        return visited[node.val]
