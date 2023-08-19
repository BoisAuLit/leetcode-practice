from typing import Optional

"""
Time complexity: O()
Space complexity: O()
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        return 1 + self.countNodes(root.left) + self.countNodes(root.right)
