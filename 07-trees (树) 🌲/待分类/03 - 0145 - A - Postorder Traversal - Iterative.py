from TreeNode import TreeNode

class Solution_Recursive:
    def postorderTraversal(self, root):
        result = []

        def dfs(node: TreeNode):
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            result.append(node.val)

        dfs(root)
        return result


class Solution_Iterative:
    def postorderTraversal(self, root):
        if not root:
            return []

        stack = [root]
        result = []

        while stack:
            node = stack.pop()
            result.append(node.val)

            # 先放 left，再放 right
            # 因为 stack 是 LIFO，所以 right 会先被处理
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

        return result[::-1]
