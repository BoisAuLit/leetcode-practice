from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right



"""
✅ Preferred solution: 唯一简单解
"""
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        stack = [(p, q)]

        while stack:
            n1, n2 = stack.pop()

            if not n1 and not n2:
                continue

            if not n1 or not n2:
                return False

            if n1.val != n2.val:
                return False

            stack.append((n1.left, n2.left))
            stack.append((n1.right, n2.right))

        return True

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if not subRoot:
            return True

        if not root:
            return False

        stack = [root]

        while stack:
            node = stack.pop()

            if node.val == subRoot.val and self.isSameTree(node, subRoot):
                return True

            if node.left:
                stack.append(node.left)

            if node.right:
                stack.append(node.right)

        return False
