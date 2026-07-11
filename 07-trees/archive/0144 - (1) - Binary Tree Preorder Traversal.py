from typing import List, Optional
from TreeNode import TreeNode


class Solution_Iterative:
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

##############################################################################
##############################################################################

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

##############################################################################
##############################################################################

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
