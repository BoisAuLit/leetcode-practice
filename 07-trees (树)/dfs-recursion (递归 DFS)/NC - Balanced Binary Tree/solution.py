from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution_DFS_Recursive_1:
    def __init__(self):
        self.balancedMap = {None: True}
        self.heightMap = {None: 0}

    def height(self, root: Optional[TreeNode]) -> bool:
        if root in self.heightMap:
            return self.heightMap[root]
        res = 1 + max(self.height(root.left), self.height(root.right))
        self.heightMap[root] = res
        return res

    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if root in self.balancedMap:
            return self.balancedMap[root]
        r1 = self.isBalanced(root.left)
        r2 = self.isBalanced(root.right)
        h1 = self.height(root.left)
        h2 = self.height(root.right)

        res = r1 and r2 and abs(h1 - h2) <= 1
        self.balancedMap[root] = res

        return res

class Solution_DFS_Recursive_2:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def dfs(root):
            if not root:
                return [True, 0]

            left, right = dfs(root.left), dfs(root.right)
            balanced = left[0] and right[0] and abs(left[1] - right[1]) <= 1
            return [balanced, 1 + max(left[1], right[1])]

        return dfs(root)[0]

"""
✅ Preferred method
"""
class Solution_DFS_Iterative:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        # ! First, obtain the post-order traversal
        stack = [root]
        order = []
        while stack:
            node = stack.pop()
            order.append(node)

            # 先压 left，后压 right，因此 right 先出栈
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

        heights = {None: 0}

        for node in reversed(order):
            left = heights[node.left]
            right = heights[node.right]

            if abs(left - right) > 1:
                return False

            heights[node] = 1 + max(left, right)

        return True
