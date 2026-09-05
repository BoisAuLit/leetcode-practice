from typing import Optional

"""
Time complexity: O(n)
Space complexity:
- O(1) if we don't consider the stack
- O(h) if we consider the stack (h is the height of the tree)
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        if not p or not q:
            return False
        return (
            (p.val == q.val)
            and self.isSameTree(p.left, q.left)
            and self.isSameTree(p.right, q.right)
        )


"""
Runtime
- 43 ms
- Beats 72%

Memory
- 16.3 MB
- Beats 82.37%
"""
