"""LC-0100 - Same Tree

合并自 2 个解法文件:
  1. 0100-A - (1) - Same Tree - DFS-Recursive.py
  2. 0100-B - (1) - Same Tree - BFS-Queue-Iterative 👍.py
"""

from typing import Optional

from collections import deque


# ============================================================================
# Solution 1: DFS_Recursive    (原文件: 0100-A - (1) - Same Tree - DFS-Recursive.py)
# ============================================================================

# Time complexity: O(n)
# Space complexity:
# - O(1) if we don't consider the stack
# - O(h) if we consider the stack (h is the height of the tree)

# Runtime
# - 43 ms
# - Beats 72%
#
# Memory
# - 16.3 MB
# - Beats 82.37%

class TreeNode_1:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_1_DFS_Recursive:
    def isSameTree(self, p: Optional[TreeNode_1], q: Optional[TreeNode_1]) -> bool:
        if not p and not q:
            return True
        if not p or not q:
            return False
        return (
            (p.val == q.val)
            and self.isSameTree(p.left, q.left)
            and self.isSameTree(p.right, q.right)
        )

# ============================================================================
# Solution 2: BFS_Queue_Iterative    (原文件: 0100-B - (1) - Same Tree - BFS-Queue-Iterative 👍.py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)


class TreeNode_2:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_2_BFS_Queue_Iterative:
    def isSameTree(self, p, q):
        def check(p, q):
            if not p and not q:
                return True
            if not q or not p:
                return False
            return p.val == q.val

        deq = deque([(p, q)])
        while deq:
            p, q = deq.popleft()
            if not check(p, q):
                return False

            if p:
                deq.append((p.left, q.left))
                deq.append((p.right, q.right))

        return True


if __name__ == "__main__":

    # --- Solution 2: BFS_Queue_Iterative ---
    t1 = TreeNode_2(1, TreeNode_2(3, TreeNode_2(7), TreeNode_2(9)), TreeNode_2(5))
    t2 = TreeNode_2(1, TreeNode_2(3, TreeNode_2(7), TreeNode_2(8)), TreeNode_2(5))
    s = Solution_2_BFS_Queue_Iterative()
    output = s.isSameTree(t1, t2)
    print(output)
