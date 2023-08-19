from typing import Optional


"""
Time complexity: O(n)
Space complexity: O(n)
"""

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        if bool(root.left) + bool(root.right) == 1:
            return 1 + self.minDepth(root.left if root.left else root.right)
        if not root.left and not root.right:
            return 1
        return 1 + min(self.minDepth(root.left), self.minDepth(root.right))


# Expecting 5 as result
input_ = TreeNode(
    2,
    None,
    TreeNode(3, None, TreeNode(4, None, TreeNode(5, None, TreeNode(6)))),
)
s = Solution()
result = s.minDepth(input_)
print(result)

"""
Runtime
- 566 ms
- Beats 60.58%

Memory
- 57.3 MB
- Beats 18.11%
"""
