from typing import Optional
from TreeNode import TreeNode

"""
The following 2 solutions are non-optimal
"""


class Solution_Recursive:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        arr = []

        def dfs(node):
            if not node:
                return

            dfs(node.left)
            arr.append(node.val)
            dfs(node.right)

        dfs(root)
        return arr[k - 1]


class Solution_Iterative:
    def inorderTraversal(self, root):
        result = []
        stack = []
        curr = root
        while curr or stack:  # 这一步非常非常关键
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            result.append(curr.val)
            curr = curr.right
        return result

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        array = self.inorderTraversal(root)
        return array[k - 1]


"""
The following 2 solutions are optimal
"""


class Solution_DFS_Recursive:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        res = root.val

        def dfs(node):
            nonlocal k, res
            if not node:
                return

            dfs(node.left)
            if k == 0:
                return
            k -= 1
            if k == 0:
                res = node.val
                return
            dfs(node.right)

        dfs(root)
        return res


"""
✅ This is the preferred solution
"""
class Solution_DFS_Iterative:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        curr = root

        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            k -= 1
            if k == 0:
                return curr.val
            curr = curr.right
