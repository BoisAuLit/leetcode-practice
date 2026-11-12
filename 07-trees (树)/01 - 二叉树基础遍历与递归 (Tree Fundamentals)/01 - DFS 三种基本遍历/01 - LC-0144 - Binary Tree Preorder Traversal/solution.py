"""LC-0144 - Binary Tree Preorder Traversal

合并自 2 个解法文件:
  1. 0144 - (1) - Binary Tree Preorder Traversal.py
  2. 01 - 0144 - A - Preorder Traversal - Iterative.py
"""

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
# Solution 1: Binary_Tree_Preorder_Traversal    (原文件: 0144 - (1) - Binary Tree Preorder Traversal.py)
# ============================================================================

class Solution_Iterative_1:
    """
    Let N be the number of nodes in the tree
    - Time complexity: O(N)
    - Space complexity: O(N)
    """

    def preorderTraversal(self, root: TreeNode) -> List[int]:
        stack, answer = [root], []
        while stack:
            curr_node = stack.pop()
            if curr_node:
                answer.append(curr_node.val)
                stack.append(curr_node.right)
                stack.append(curr_node.left)

        return answer

class Solution_Recursive_1:
    """
    Let N be the number of nodes in the tree
    - Time complexity: O(N)
    - Space complexity: O(N)
    """

    def preorderTraversal(self, root: TreeNode) -> List[int]:
        answer = []

        # dfs means depth-first search
        def dfs(node):
            if not node:
                return
            answer.append(node.val)
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return answer

class Solution_Recursive_2:
    """
    Let N be the number of nodes in the tree
    - Time complexity: O(N)
    - Space complexity: O(N)
    """

    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        return (
            [root.val]
            + self.preorderTraversal(root.left)
            + self.preorderTraversal(root.right)
        )

# ============================================================================
# Solution 2: Iterative    (原文件: 01 - 0144 - A - Preorder Traversal - Iterative.py)
# ============================================================================

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

class Solution_Iterative_2:
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
