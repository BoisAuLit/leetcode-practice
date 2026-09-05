from typing import Optional
from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution_DFS_Recursive:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        if p and q and p.val == q.val:
            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        else:
            return False


"""
✅ Preferred method
"""
class Solution_DFS_Iterative_Stack:
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


class Solution_BFS_Iterative_Queue:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        dq = deque([(p, q)])

        while dq:
            n1, n2 = dq.popleft()

            if not n1 and not n2:
                continue

            if not n1 or not n2:
                return False

            if n1.val != n2.val:
                return False

            dq.append((n1.left, n2.left))
            dq.append((n1.right, n2.right))

        return True
