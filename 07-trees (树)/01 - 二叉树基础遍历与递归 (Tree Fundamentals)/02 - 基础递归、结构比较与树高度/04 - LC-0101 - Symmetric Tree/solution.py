"""LC-0101 - Symmetric Tree

合并自 4 个解法文件:
  1. 0101-A - (1) - Symmetric Tree - (Iterative) 👍.py
  2. 0101-B - (1) - Symmetric Tree - (Recursive).py
  3. 06 - 0101 - A - Symmetric Tree - Iterative Queue.py
  4. 06 - 0101 - B - Symmetric Tree - Recursive.py
"""

from typing import Optional

from collections import deque

# ! ---------------------------------------------------------------------------------------------
# ! 下面这个 TreeNode 是本次重构补上的：原文件底部的示例代码用到了 TreeNode.from_list /
# ! printTree，但文件里没有定义（或定义里缺这些方法），运行时直接报 NameError / AttributeError。
# ! 定义取自本专题的 utils/TreeNode.py，**没有改动任何解法代码**。
# ! ---------------------------------------------------------------------------------------------
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    @staticmethod
    def from_list(values):
        """LeetCode 的层序数组表示（None 表示空位）-> 树根。"""
        if not values or values[0] is None:
            return None
        root = TreeNode(values[0])
        queue = [root]
        i = 1
        while queue and i < len(values):
            node = queue.pop(0)
            if i < len(values):
                if values[i] is not None:
                    node.left = TreeNode(values[i])
                    queue.append(node.left)
                i += 1
            if i < len(values):
                if values[i] is not None:
                    node.right = TreeNode(values[i])
                    queue.append(node.right)
                i += 1
        return root

    @staticmethod
    def to_list(root):
        """树 -> 层序数组（去掉尾部多余的 None），方便对拍。"""
        if not root:
            return []
        out, queue = [], [root]
        while queue:
            node = queue.pop(0)
            if node:
                out.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                out.append(None)
        while out and out[-1] is None:
            out.pop()
        return out

    def printTree(self):
        print("TreeNode ->", TreeNode.to_list(self))



# ============================================================================
# Solution 1: Iterative    (原文件: 0101-A - (1) - Symmetric Tree - (Iterative) 👍.py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

# Runtime
# - 46 ms
# - Beats 77.66%
#
# Memory
# - 16.6 MB
# - Beats 8.83%

class TreeNode_1:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_1_Iterative:
    def tree_node_equal(self, t1: TreeNode_1, t2: TreeNode_1) -> bool:
        if not t1 and not t2:
            return True
        if t1 and t2:
            return t1.val == t2.val
        return False

    def isSymmetric(self, root: Optional[TreeNode_1]) -> bool:
        deq1 = deque([root.left])
        deq2 = deque([root.right])
        while deq1 and deq2:
            node1 = deq1.popleft()
            node2 = deq2.popleft()
            if not self.tree_node_equal(node1, node2):
                return False
            if node1 and node2:
                deq1.append(node1.left)
                deq1.append(node1.right)
                deq2.append(node2.right)
                deq2.append(node2.left)

        return not deq1 and not deq2

# ============================================================================
# Solution 2: V2    (原文件: 0101-B - (1) - Symmetric Tree - (Recursive).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

# Runtime
# - 55 ms
# - Beats 27.64%
#
# Memory
# - 16.4 MB
# - Beats 39.36%

class TreeNode_2:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_2_V2:
    def are_symmetric(
        self, t1: Optional[TreeNode_2], t2: Optional[TreeNode_2]
    ) -> bool:
        if not t1 and not t2:
            return True
        if t1 and t2:
            return (
                t1.val == t2.val
                and self.are_symmetric(t1.left, t2.right)
                and self.are_symmetric(t1.right, t2.left)
            )
        return False

    def isSymmetric(self, root: Optional[TreeNode_2]) -> bool:
        if not root:
            return True
        return self.are_symmetric(root.left, root.right)

# ============================================================================
# Solution 3: Iterative_Queue    (原文件: 06 - 0101 - A - Symmetric Tree - Iterative Queue.py)
# ============================================================================

class Solution_3_Iterative_Queue:
    def isSymmetric(self, root):
        queue = deque([root, root])
        while queue:
            t1 = queue.popleft()
            t2 = queue.popleft()
            if not t1 and not t2:
                continue
            if not t1 or not t2:
                return False
            if t1.val != t2.val:
                return False
            queue.append(t1.left)
            queue.append(t2.right)
            queue.append(t1.right)
            queue.append(t2.left)
        return True

# ============================================================================
# Solution 4: B    (原文件: 06 - 0101 - B - Symmetric Tree - Recursive.py)
# ============================================================================

class Solution_4_B:
    def isSymmetric(self, root):
        def dfs(t1, t2):
            if not t1 and not t2:
                return True
            if bool(t1) != bool(t2):
                return False
            return (
                (t1.val == t2.val)
                and dfs(t1.right, t2.left)
                and dfs(t1.left, t2.right)
            )

        return dfs(root.left, root.right)


if __name__ == "__main__":

    # --- Solution 1: Iterative ---
    tree_symmetric = TreeNode_1(
        1,
        TreeNode_1(3, None, TreeNode_1(5, TreeNode_1(7, TreeNode_1(9), TreeNode_1(8)), None)),
        TreeNode_1(3, TreeNode_1(5, None, TreeNode_1(7, TreeNode_1(8), TreeNode_1(9))), None),
    )
    tree_asymmetric = TreeNode_1(
        1,
        TreeNode_1(3, None, TreeNode_1(5, TreeNode_1(7, TreeNode_1(6), TreeNode_1(8)), None)),
        TreeNode_1(3, TreeNode_1(5, None, TreeNode_1(7, TreeNode_1(8), TreeNode_1(9))), None),
    )
    tree_asymmetric_2 = TreeNode_1(
        1, TreeNode_1(2, None, TreeNode_1(3)), TreeNode_1(2, None, TreeNode_1(3))
    )
    s = Solution_1_Iterative()
    result = s.isSymmetric(tree_asymmetric) # Expecting False
    print(result)
    s = Solution_1_Iterative()
    result = s.isSymmetric(tree_asymmetric_2) # Expecting False
    print(result)

    # --- Solution 2: V2 ---
    tree_symmetric = TreeNode_2(
        1,
        TreeNode_2(3, None, TreeNode_2(5, TreeNode_2(7, TreeNode_2(9), TreeNode_2(8)), None)),
        TreeNode_2(3, TreeNode_2(5, None, TreeNode_2(7, TreeNode_2(8), TreeNode_2(9))), None),
    )
    tree_asymmetric = TreeNode_2(
        1,
        TreeNode_2(3, None, TreeNode_2(5, TreeNode_2(7, TreeNode_2(6), TreeNode_2(8)), None)),
        TreeNode_2(3, TreeNode_2(5, None, TreeNode_2(7, TreeNode_2(8), TreeNode_2(9))), None),
    )
    tree_asymmetric_2 = TreeNode_2(
        1, TreeNode_2(2, None, TreeNode_2(3)), TreeNode_2(2, None, TreeNode_2(3))
    )
    s = Solution_2_V2()
    result = s.isSymmetric(tree_asymmetric)  # Expecting False
    print(result)
    s = Solution_2_V2()
    result = s.isSymmetric(tree_asymmetric_2)  # Expecting False
    print(result)

    # --- Solution 3: Iterative_Queue ---
    s = Solution_3_Iterative_Queue()
    node = TreeNode.from_list([1, 2, 2, None, 3, None, 3])
    TreeNode.printTree(node)
    result = s.isSymmetric(node)
    print(result)

    # --- Solution 4: B ---
    s = Solution_4_B()
    node = TreeNode.from_list([1, 2, 2, None, 3, None, 3])
    TreeNode.printTree(node)
    result = s.isSymmetric(node)
    print(result)
