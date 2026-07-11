from typing import List, Optional
from TreeNode import TreeNode

class Solution:
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


# Test case 1: Expecting [1,2,4,5,6,7,3,8,9]
root = TreeNode.from_list([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
TreeNode.printTree(root)
s = Solution()
result = s.preorderTraversal(root)
print(result)
