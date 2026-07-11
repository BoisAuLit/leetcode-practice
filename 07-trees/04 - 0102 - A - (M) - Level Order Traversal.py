from typing import Optional, List
from TreeNode import TreeNode
from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        result = []
        queue = deque([root])
        while queue:
            tmp = []
            for _ in range(len(queue)):
                node = queue.popleft()
                tmp.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(tmp)
        return result

root = TreeNode.from_list([3, 9, 20, None, None, 15, 7])
TreeNode.printTree(root)
s = Solution()
result = s.levelOrder(root)
print(result)

