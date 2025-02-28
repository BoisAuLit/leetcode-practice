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


class Solution:
    def cloneGraph(self, node: "Node") -> "Node":
        if not node:
            return node

        queue, clones = deque([node]), {node.val: Node(node.val, [])}
        while queue:
            cur = queue.popleft()
            cur_clone = clones[cur.val]

            for ngbr in cur.neighbors:
                if ngbr.val not in clones:
                    clones[ngbr.val] = Node(ngbr.val, [])
                    queue.append(ngbr)

                cur_clone.neighbors.append(clones[ngbr.val])

        return clones[node.val]


# Solution: Using adjacency list, BFS using Queue
# class Solution:
#     def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
#         if not node:
#             return None
#         queue = deque([node])
#         visited = set([node.val])
#         adjacency_list = dict()
#         while queue:
#             curr = queue.popleft()
#             adjacency_list[curr.val] = [x.val for x in curr.neighbors]
#             for neighbor in curr.neighbors:
#                 if neighbor.val not in visited:
#                     visited.add(neighbor.val)
#                     queue.append(neighbor)
#         nodes = [Node(i) for i in range(1, len(adjacency_list) + 1)]
#         for i, neighbors in adjacency_list.items():
#             nodes[i - 1].neighbors = [nodes[j - 1] for j in neighbors]
#         return nodes[0]


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
