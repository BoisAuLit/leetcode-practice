from typing import List
from TreeNode import TreeNode


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


##############################################################################
##############################################################################


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


##############################################################################
##############################################################################


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


s = Solution_Recursive_1()
input_ = TreeNode(1, None, TreeNode(2, TreeNode(3), None))
result = s.postorderTraversal(input_)
print(result)
