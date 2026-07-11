from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False
        if targetSum == root.val and not root.left and not root.right:
            return True
        complement = targetSum - root.val
        return self.hasPathSum(root.left, complement) or self.hasPathSum(
            root.right, complement
        )
