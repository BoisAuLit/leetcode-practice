"""LC-0110 - Balanced Binary Tree

合并自 2 个解法文件:
  1. 0110-A - Balanced Binary Tree - (Top Down).py
  2. 0110-B - Balanced Binary Tree - (Bottom Up).py
"""

from typing import Optional, Tuple


# ============================================================================
# Solution 1: Top_Down    (原文件: 0110-A - Balanced Binary Tree - (Top Down).py)
# ============================================================================

# Time complexity: O(nlogn)
# Space complexity: O(n)

class TreeNode_1:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_1_Top_Down:
    def height(self, root: Optional[TreeNode_1]) -> int:
        if not root:
            return 0
        return 1 + max(self.height(root.left), self.height(root.right))

    def isBalanced(self, root: Optional[TreeNode_1]) -> bool:
        if not root:
            return True
        return (
            abs(self.height(root.left) - self.height(root.right)) <= 1
            and self.isBalanced(root.left)
            and self.isBalanced(root.right)
        )

# ============================================================================
# Solution 2: Bottom_Up    (原文件: 0110-B - Balanced Binary Tree - (Bottom Up).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(,)

class TreeNode_2:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_2_Bottom_Up:
    def isBalancedHelper(self, root: Optional[TreeNode_2]) -> Tuple[bool, int]:
        if not root:
            return True, -1

        leftIsBalanced, leftHeight = self.isBalancedHelper(root.left)
        if not leftIsBalanced:
            return False, 0
        rightIsBalanced, rightHeight = self.isBalancedHelper(root.right)
        if not rightIsBalanced:
            return False, 0

        return (abs(leftHeight - rightHeight) < 2), 1 + max(
            leftHeight, rightHeight
        )

    def isBalanced(self, root: TreeNode_2) -> bool:
        return self.isBalancedHelper(root)[0]


if __name__ == "__main__":

    # --- Solution 2: Bottom_Up ---
    t = TreeNode_2(3,
                 TreeNode_2(4, TreeNode_2(6), TreeNode_2(7, TreeNode_2(9), TreeNode_2(10))),
                 TreeNode_2(5, None, TreeNode_2(8)))
    s = Solution_2_Bottom_Up()
    result = s.isBalanced(t)
    print(result)
