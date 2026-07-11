"""
https://leetcode.com/problems/binary-tree-inorder-traversal/
"""


class Solution:
    def inorderTraversal(self, root):
        result = []

        def dfs(node):
            if node:
                dfs(node.left)
                result.append(node.val)
                dfs(node.right)

        dfs(root)
        return result
