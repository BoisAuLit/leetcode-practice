"""LC-0112 - Path Sum

合并自 3 个解法文件:
  1. 0112 - Path Sum.py
  2. 07 - 0112 - A - Path Sum - Recursive.py
  3. 07 - 0112 - B - Path Sum - Iterative - Preorder.py
"""

from typing import Optional


# ============================================================================
# Solution 1: Path_Sum    (原文件: 0112 - Path Sum.py)
# ============================================================================

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_1_Path_Sum:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False
        if targetSum == root.val and not root.left and not root.right:
            return True
        complement = targetSum - root.val
        return self.hasPathSum(root.left, complement) or self.hasPathSum(
            root.right, complement
        )

# ============================================================================
# Solution 2: Recursive    (原文件: 07 - 0112 - A - Path Sum - Recursive.py)
# ============================================================================

class Solution_2_Recursive:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        if not root:
            return False

        sum -= root.val
        if not root.left and not root.right:  # if reach a leaf
            return sum == 0
        return self.hasPathSum(root.left, sum) or self.hasPathSum(
            root.right, sum
        )

# ============================================================================
# Solution 3: Preorder    (原文件: 07 - 0112 - B - Path Sum - Iterative - Preorder.py)
# ============================================================================

class Solution_3_Preorder:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        if not root:
            return False

        stack = [(root, sum - root.val)]
        while stack:
            node, curr_sum = stack.pop()
            if not node.left and not node.right and curr_sum == 0:
                return True
            if node.right:
                stack.append((node.right, curr_sum - node.right.val))
            if node.left:
                stack.append((node.left, curr_sum - node.left.val))
        return False
