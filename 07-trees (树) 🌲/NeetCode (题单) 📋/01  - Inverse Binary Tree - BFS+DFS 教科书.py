from typing import Optional
from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


"""
DFS methods:
1. Recursive
2. Iterative (with stack)
"""


class Solution_DFS_Recursive:
    """
    ! This method is the most intuitive one
    """
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return root
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root


class Solution_DFS_Iterative_Stack:
    """
    Last in first out (LIFO) 🚦
    Remove itself and append its left/right children
    0. [root] # ! Python's list is stak by nature
    1. pop()
    2. append()
    """
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        stack = [root]
        while stack:
            node = stack.pop()
            node.left, node.right = node.right, node.left
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return root


class Solution_BFS_Queue_Iterative:
    """
    First in first out (FIFO) 🚥
    Remove itself and append its left/right children
    0. deque([root]) # ! We need to import python deque to achieve this
    1. popleft()
    2. append()
    """
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        queue = deque([root])
        while queue:
            node = queue.popleft()
            node.left, node.right = node.right, node.left
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return root
