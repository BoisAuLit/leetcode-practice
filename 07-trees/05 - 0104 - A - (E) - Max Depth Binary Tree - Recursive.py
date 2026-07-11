from typing import Optional
from TreeNode import TreeNode


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0
            return 1 + max(dfs(node.left), dfs(node.right))
        return dfs(root)
