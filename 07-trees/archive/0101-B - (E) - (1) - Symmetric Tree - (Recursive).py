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
    def are_symmetric(
        self, t1: Optional[TreeNode], t2: Optional[TreeNode]
    ) -> bool:
        if not t1 and not t2:
            return True
        if t1 and t2:
            return (
                t1.val == t2.val
                and self.are_symmetric(t1.left, t2.right)
                and self.are_symmetric(t1.right, t2.left)
            )
        return False

    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        return self.are_symmetric(root.left, root.right)


tree_symmetric = TreeNode(
    1,
    TreeNode(3, None, TreeNode(5, TreeNode(7, TreeNode(9), TreeNode(8)), None)),
    TreeNode(3, TreeNode(5, None, TreeNode(7, TreeNode(8), TreeNode(9))), None),
)

tree_asymmetric = TreeNode(
    1,
    TreeNode(3, None, TreeNode(5, TreeNode(7, TreeNode(6), TreeNode(8)), None)),
    TreeNode(3, TreeNode(5, None, TreeNode(7, TreeNode(8), TreeNode(9))), None),
)

tree_asymmetric_2 = TreeNode(
    1, TreeNode(2, None, TreeNode(3)), TreeNode(2, None, TreeNode(3))
)

# Testing symmetric
# s = Solution()
# result = s.isSymmetric(tree_symmetric) # Expecting True
# print(result)

# Testing asymmetric
s = Solution()
result = s.isSymmetric(tree_asymmetric)  # Expecting False
print(result)


# Testing ssymmetric 2
s = Solution()
result = s.isSymmetric(tree_asymmetric_2)  # Expecting False
print(result)


"""
Runtime
- 55 ms
- Beats 27.64%

Memory
- 16.4 MB
- Beats 39.36%
"""
