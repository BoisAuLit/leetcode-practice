from TreeNode import TreeNode


class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        if not root:
            return False

        stack = [(root, sum - root.val)]
        while stack:
            node, curr_sum = stack.pop()
            if not node.left and not node.right and curr_sum == 0:
                return True
            if node.right:
                stack.append((node.right, curr_sum - node.right.val))
            if node.left:
                stack.append((node.left, curr_sum - node.left.val))
        return False
