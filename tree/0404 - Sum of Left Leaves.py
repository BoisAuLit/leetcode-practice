from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sumOfLeftLeaves(self, root: TreeNode) -> int:
        if root is None:
            return 0

        def is_leaf(node):
            return node and not node.left and not node.right

        stack = [root]
        total = 0
        while stack:
            curr = stack.pop()
            if curr:
                if is_leaf(curr.left):
                    total += curr.left.val
                stack.append(curr.right)
                stack.append(curr.left)

        return total


# class Solution:
#     def sumOfLeftLeaves(self, root: Optional[TreeNode]) -> int:
#         if not root or (not root.left and not root.right):
#             return 0
#         if root.left and not root.left.left and not root.left.right:
#             return root.left.val + self.sumOfLeftLeaves(root.right)
#         else:
#             return self.sumOfLeftLeaves(root.left) + self.sumOfLeftLeaves(
#                 root.right
#             )


s = Solution()

# Expecting 24
input_ = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))

result = s.sumOfLeftLeaves(input_)
print(result)

"""

"""
