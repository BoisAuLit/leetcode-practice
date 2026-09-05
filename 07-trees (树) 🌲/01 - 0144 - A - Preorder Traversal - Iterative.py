from typing import List, Optional
from TreeNode import TreeNode


class Solution_Recursive:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        result = []

        def dfs(node: Optional[TreeNode]):
            if not node:
                return
            result.append(node.val)
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return result

class Solution_Iterative:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        stack = [root]
        result = []
        while stack:
            node = stack.pop()
            result.append(node.val)
            # ! Here it is important, must put right first
            # ! Because it's LIFO (stack) - Reverse order
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result
