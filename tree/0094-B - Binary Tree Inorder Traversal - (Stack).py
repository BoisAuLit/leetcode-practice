from typing import List, Optional


"""
Time complexity: O(n)
Space complexity: O(n)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        curr = root
        res = []
        stack = []
        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            res.append(curr.val)
            curr = curr.right
        return res


s = Solution()
input_ = TreeNode(1, None, TreeNode(2, TreeNode(3), None))
result = s.inorderTraversal(input_)
print(result)

"""
Runtime
- 57 ms
- Beats 6.11%

Memory
- 16.4 MB
- Beats 27.4%
"""
