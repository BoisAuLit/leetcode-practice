from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_DFS_Stack:
    """
    Pre-order traversal
    """
    def goodNodes(self, root: TreeNode) -> int:
        stack = [(root, root.val)]
        res = 0
        while stack:
            node, maxSince = stack.pop()
            if node.val >= maxSince:
                res += 1
            if node.left:
                stack.append((node.left, max(maxSince, node.left.val)))
            if node.right:
                stack.append((node.right, max(maxSince, node.right.val)))
        return res

class Solution_BFS_Queue:
    def goodNodes(self, root: TreeNode) -> int:
        dq = deque([(root, root.val)])
        res = 0
        while dq:
            for _ in range(len(dq)):
                node, maxSince = dq.popleft()
                if node.val >= maxSince:
                    res += 1
                if node.left:
                    dq.append((node.left, max(maxSince, node.left.val)))
                if node.right:
                    dq.append((node.right, max(maxSince, node.right.val)))
        return res
