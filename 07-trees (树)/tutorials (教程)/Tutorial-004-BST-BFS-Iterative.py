from TreeNode import TreeNode
from collections import deque

class BFS_Iterative:
    def bfs(self, root: TreeNode):
        if not root:
            return []
        result = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            result.append(node.val)
            print(node.val, end=" ")
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

s = BFS_Iterative()

treeNode = TreeNode.from_list(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'])
print("Original tree:")
treeNode.printTree()

print("\nBFS Iterative:   ", end=" ")
s.bfs(treeNode)
