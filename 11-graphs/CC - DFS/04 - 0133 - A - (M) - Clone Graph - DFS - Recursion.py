from typing import Optional


class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


"""
DFS Iterative approach is declarative style

"""

class Solution:

    def __init__(self):
        # ! The key is original node
        # ! The value is the cloned ndoe
        # * This helps avoid cycles 🔄
        self.visited = {}

    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if not node:
            return node

        # If the node was already visited before.
        # Return the clone from the visited dictionary.
        if node in self.visited:
            return self.visited[node] 

        # Create a clone for the given node.
        # Note that we don't have cloned neighbors as of now, hence [].
        clone_node = Node(node.val, [])
        
        # ! The key is original node
        # ! The value is the cloned ndoe
        self.visited[node] = clone_node

        # Iterate over the neighbors to generate their clones
        # and prepare a list of cloned neighbors to be added to the cloned node.
        # ! For each node, we also make sure that its clone also copies its neighbors
        # ! For each neighbor of the original node, we also create a clone neighbor for the cloned node
        if node.neighbors:
            clone_node.neighbors = [self.cloneGraph(n) for n in node.neighbors]

        return clone_node

node1 = Node(1, [])
node2 = Node(2, [])
node3 = Node(3, [])
node4 = Node(4, [])

node1.neighbors = [node2, node4]
node3.neighbors = [node2, node4]
node2.neighbors = [node1, node3]
node4.neighbors = [node1, node3]
s = Solution()
result = s.cloneGraph(node1)
print(node1)
