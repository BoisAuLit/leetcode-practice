from typing import Optional
from collections import deque

"""
Time complexity: O(n)
Space complexity: O(n)
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution(object):
    def minDepth(self, root: Optional[TreeNode]):
        if not root:
            return 0
        queue = deque([[root, 1]])
        while queue:
            node, depth = queue.popleft()
            if not node.left and not node.right:
                return depth
            if node.left:
                queue.append([node.left, depth + 1])
            if node.right:
                queue.append([node.right, depth + 1])


# Expecting 5 as result
input_ = TreeNode(
    2,
    None,
    TreeNode(3, None, TreeNode(4, None, TreeNode(5, None, TreeNode(6)))),
)
s = Solution()
result = s.minDepth(input_)
print(result)

"""
Runtime
- 472 ms
- Beats 95.14%

Memory
- 51.6 MB
- Beats 77.25%
"""
