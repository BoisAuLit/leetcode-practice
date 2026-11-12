"""LC-0145 - Binary Tree Postorder Traversal

合并自 2 个解法文件:
  1. 0145 - (1) - Binary Tree Postorder Traversal.py
  2. 03 - 0145 - A - Postorder Traversal - Iterative.py
"""

from typing import List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
# Solution 1: Binary_Tree_Postorder_Traversal    (原文件: 0145 - (1) - Binary Tree Postorder Traversal.py)
# ============================================================================

class Solution_Iterative_1(object):
    def postorderTraversal(self, root: TreeNode) -> List[int]:
        stack, answer = [root], []
        while stack:
            root = stack.pop()
            if root:
                stack.append(root.left)
                stack.append(root.right)
                answer.append(root.val)
        return answer[::-1]

class Solution_Recursive_1:
    """
    Let N be the number of nodes in the tree
    - Time complexity: O(N)
    - Space complexity: O(N)
    """

    def postorderTraversal(self, root: TreeNode) -> List[int]:
        answer = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            answer.append(node.val)

        dfs(root)
        return answer

class Solution_Recursive_2:
    """
    Let N be the number of nodes in the tree
    - Time complexity: O(N)
    - Space complexity: O(N)
    """

    def postorderTraversal(self, root: TreeNode) -> List[int]:
        if not root:
            return []
        return (
            self.postorderTraversal(root.left)
            + self.postorderTraversal(root.right)
            + [root.val]
        )

# ============================================================================
# Solution 2: Iterative    (原文件: 03 - 0145 - A - Postorder Traversal - Iterative.py)
# ============================================================================

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


if __name__ == "__main__":

    # --- Solution 1: Binary_Tree_Postorder_Traversal ---
    s = Solution_Recursive_1()
    input_ = TreeNode(1, None, TreeNode(2, TreeNode(3), None))
    result = s.postorderTraversal(input_)
    print(result)
