"""LC-0111 - Minimum Depth of Binary Tree

合并自 2 个解法文件:
  1. 0111-A - Minimum Depth Of Binary Tree - (Depth-First Search).py
  2. 0111-B - Minimum Depth Of Binary Tree - (Breadth-First Search 👍).py
"""

from typing import Optional

from collections import deque


# ============================================================================
# Solution 1: Depth_First_Search    (原文件: 0111-A - Minimum Depth Of Binary Tree - (Depth-First Search).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

# Runtime
# - 566 ms
# - Beats 60.58%
#
# Memory
# - 57.3 MB
# - Beats 18.11%

class TreeNode_1:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_1_Depth_First_Search:
    def minDepth(self, root: Optional[TreeNode_1]) -> int:
        if not root:
            return 0
        if bool(root.left) + bool(root.right) == 1:
            return 1 + self.minDepth(root.left if root.left else root.right)
        if not root.left and not root.right:
            return 1
        return 1 + min(self.minDepth(root.left), self.minDepth(root.right))

# ============================================================================
# Solution 2: Breadth_First_Search    (原文件: 0111-B - Minimum Depth Of Binary Tree - (Breadth-First Search 👍).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

# Runtime
# - 472 ms
# - Beats 95.14%
#
# Memory
# - 51.6 MB
# - Beats 77.25%

class TreeNode_2:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_2_Breadth_First_Search(object):
    def minDepth(self, root: Optional[TreeNode_2]):
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


if __name__ == "__main__":

    # --- Solution 1: Depth_First_Search ---
    input_ = TreeNode_1(
        2,
        None,
        TreeNode_1(3, None, TreeNode_1(4, None, TreeNode_1(5, None, TreeNode_1(6)))),
    )
    s = Solution_1_Depth_First_Search()
    result = s.minDepth(input_)
    print(result)

    # --- Solution 2: Breadth_First_Search ---
    input_ = TreeNode_2(
        2,
        None,
        TreeNode_2(3, None, TreeNode_2(4, None, TreeNode_2(5, None, TreeNode_2(6)))),
    )
    s = Solution_2_Breadth_First_Search()
    result = s.minDepth(input_)
    print(result)
