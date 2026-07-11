from typing import List, Optional
from TreeNode import TreeNode


class Solution:
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


# Test case 1: Expecting [1,2,4,5,6,7,3,8,9]
root = TreeNode.from_list([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
TreeNode.printTree(root)
s = Solution()
result = s.preorderTraversal(root)
print(result)
