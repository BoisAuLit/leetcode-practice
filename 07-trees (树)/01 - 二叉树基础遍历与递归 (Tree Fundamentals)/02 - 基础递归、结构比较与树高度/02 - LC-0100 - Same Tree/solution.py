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


##################################################################################################
##### ! Solution NC: 迭代 DFS（显式栈）—— 来自原 NC 目录，用户自己标注为 ✅ Preferred method
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 和上面两个解法的区别：Solution_1 是递归 DFS，Solution_2 是 BFS 队列，
#####   这一份是**显式栈的迭代 DFS**，本文件原先没有，是 NC 版本独有的。
##### ! 来源：原 `NC - Same Binary Tree` 目录。按仓库规则「LC / NC 重复时只保留 LeetCode 版」，
#####   NC 文件夹已删除，但它独有的这份实现一字未改地并入这里，没有丢失任何代码。
##### ! 注：这里用的 TreeNode 是本文件上面定义的 TreeNode_1 / TreeNode_2 的任意一个皆可，
#####   三个类的字段完全相同。
##################################################################################################


TreeNode = TreeNode_1   # ! 别名：NC 版代码里写的是 TreeNode，本文件把它指向 TreeNode_1（字段完全相同）


class Solution_NC_DFS_Iterative_Stack:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        stack = [(p, q)]

        while stack:
            n1, n2 = stack.pop()

            if not n1 and not n2:
                continue

            if not n1 or not n2:
                return False

            if n1.val != n2.val:
                return False

            stack.append((n1.left, n2.left))
            stack.append((n1.right, n2.right))

        return True
