from typing import Optional, Tuple


"""
Time complexity: O(n)
Space complexity: O(,)
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isBalancedHelper(self, root: Optional[TreeNode]) -> Tuple[bool, int]:
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

    def isBalanced(self, root: TreeNode) -> bool:
        return self.isBalancedHelper(root)[0]

t = TreeNode(3,
             TreeNode(4, TreeNode(6), TreeNode(7, TreeNode(9), TreeNode(10))),
             TreeNode(5, None, TreeNode(8)))
s = Solution()
result = s.isBalanced(t)
print(result)
