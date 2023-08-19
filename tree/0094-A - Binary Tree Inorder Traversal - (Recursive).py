from typing import List, Optional


"""
Time complexity: O(n)
Space complexity: O(n)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        if not root.left and not root.right:
            return [root.val]
        return (
            self.inorderTraversal(root.left)
            + [root.val]
            + self.inorderTraversal(root.right)
        )


s = Solution()
input_ = TreeNode(1, None, TreeNode(2, TreeNode(3), None))
result = s.inorderTraversal(input_)
print(result)

"""
Runtime
- 49 ms
- Beats 34.66%

Memory
- 16.2 MB
- Beats 65.67%
"""
