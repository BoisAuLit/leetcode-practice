"""
https://leetcode.com/problems/binary-tree-inorder-traversal/
"""


class Solution:
    def inorderTraversal(self, root):
        result = []
        stack = []
        curr = root
        while curr or stack: # 这一步非常非常关键
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            result.append(curr.val)
            curr = curr.right
        return result
