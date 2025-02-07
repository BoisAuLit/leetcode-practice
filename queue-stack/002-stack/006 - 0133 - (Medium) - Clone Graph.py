from typing import Optional
from collections import deque


# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def print(self) -> None:
        print(f"Self: {self.val}")
        print("Neighbors:")
        for neighbor in self.neighbors:
            print("\t", neighbor.val)
        print("-------------------------------------")


# Solution: Using adjacency list, DFS using Stack
class Solution:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if not node:
            return None

        stack = deque([node])
        visited = set()
        adjacency_list = dict()
        while stack:
            curr = stack.pop()
            visited.add(curr.val)
            adjacency_list[curr.val] = [x.val for x in curr.neighbors]
            for neighbor in curr.neighbors:
                if neighbor.val not in visited:
                    visited.add(neighbor.val)
                    stack.append(neighbor)
        nodes = [Node(i) for i in range(1, len(adjacency_list) + 1)]
        for i, neighbors in adjacency_list.items():
            nodes[i - 1].neighbors = [nodes[j - 1] for j in neighbors]
        return nodes[0]


n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)
n1.neighbors = [n2, n4]
n2.neighbors = [n1, n3]
n3.neighbors = [n2, n4]
n4.neighbors = [n1, n3]


s = Solution()
result = s.cloneGraph(n1)
