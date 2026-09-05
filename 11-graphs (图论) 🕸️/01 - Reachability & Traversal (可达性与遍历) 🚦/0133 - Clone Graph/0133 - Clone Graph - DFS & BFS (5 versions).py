from typing import Optional
from collections import deque


# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution_DFS_Recursive:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:

        old_to_copy = {}

        def dfs(old_node):

            if old_node in old_to_copy:
                return old_to_copy[old_node]

            new_node = Node(old_node.val)
            old_to_copy[old_node] = new_node
            for old_neighbor in old_node.neighbors:
                new_node.neighbors.append(dfs(old_neighbor))

            return new_node

        return dfs(node) if node else None


class Solution_DFS_Iterative:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:

        if not node:
            return None

        old_to_copy = {node: Node(node.val)}

        stack = [node]

        while stack:
            old_node = stack.pop()

            new_node = old_to_copy[old_node]

            for old_neighbor in old_node.neighbors:
                # 第一次遇到这个邻居：创建它的克隆
                if old_neighbor not in old_to_copy:
                    old_to_copy[old_neighbor] = Node(old_neighbor.val)

                    stack.append(old_neighbor)

                # 将当前克隆节点连接到邻居的克隆节点
                new_node.neighbors.append(old_to_copy[old_neighbor])

        return old_to_copy[node]


"""
This is also the preferred solution.
"""


class Solution_BFS_1_Iteration:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:

        if not node:
            return None

        old_to_copy = {node: Node(node.val)}

        queue = deque([node])

        while queue:
            old_node = queue.popleft()

            new_node = old_to_copy[old_node]

            for old_neighbor in old_node.neighbors:
                if old_neighbor not in old_to_copy:
                    old_to_copy[old_neighbor] = Node(old_neighbor.val)

                    queue.append(old_neighbor)

                new_node.neighbors.append(old_to_copy[old_neighbor])

        return old_to_copy[node]


class Solution_DFS_2_Iterations:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if not node:
            return None
        stack = [(node)]
        adj = dict()
        max_ = 0
        while stack:
            node = stack.pop()
            max_ = max(max_, node.val)
            adj[node.val - 1] = [n.val - 1 for n in node.neighbors]
            for n in node.neighbors:
                if n.val - 1 not in adj:
                    stack.append(n)
        nodes = [Node(i + 1) for i in range(max_)]
        for i in range(max_):
            nodes[i].neighbors = [nodes[i] for i in adj[i]]
        return nodes[0]


class Solution_BFS_2_Iterations:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if not node:
            return None
        q = deque([node])
        adj = dict()
        max_ = 0
        while q:
            node = q.popleft()
            max_ = max(max_, node.val)
            adj[node.val - 1] = [n.val - 1 for n in node.neighbors]
            for n in node.neighbors:
                if n.val - 1 not in adj:
                    q.append(n)
        nodes = [Node(i + 1) for i in range(max_)]
        for i in range(max_):
            nodes[i].neighbors = [nodes[i] for i in adj[i]]

        return nodes[0]


n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n1.neighbors = [n2]
n2.neighbors = [n1, n3]
n3.neighbors = [n2]
s = Solution_DFS_Recursive()
node = n1
result = s.cloneGraph(n1)
print(result.val)
print(result.neighbors[0].val)
