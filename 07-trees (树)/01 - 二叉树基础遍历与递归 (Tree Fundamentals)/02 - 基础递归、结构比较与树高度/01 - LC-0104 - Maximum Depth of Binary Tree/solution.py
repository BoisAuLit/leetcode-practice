"""LC-0104 - Maximum Depth of Binary Tree

合并自 4 个解法文件:
  1. 0104-A - Maximum Depth Of Binary Tree - DFS-Iterative-Stack 👍.py
  2. 0104-A - Maximum Depth Of Binary Tree - Recursive.py
  3. 05 - 0104 - A - Max Depth Binary Tree - Recursive.py
  4. 05 - 0104 - B - Max Depth Binary Tree - Recursive.py
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
# Solution 1: DFS_Iterative_Stack    (原文件: 0104-A - Maximum Depth Of Binary Tree - DFS-Iterative-Stack 👍.py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(log(n))

class TreeNode_1:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_1_DFS_Iterative_Stack:
    def maxDepth(self, root: TreeNode_1) -> int:
        stack = []
        if root is not None:
            stack.append((1, root))

        depth = 0
        while stack != []:
            current_depth, root = stack.pop()
            if root is not None:
                depth = max(depth, current_depth)
                stack.append((current_depth + 1, root.left))
                stack.append((current_depth + 1, root.right))

        return depth

# ============================================================================
# Solution 2: V2    (原文件: 0104-A - Maximum Depth Of Binary Tree - Recursive.py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(log(n))

# Runtime
# - 46 ms
# - Beats 94.28%
#
# Memory
# - 18.7 MB
# - Beats 34.59%

class TreeNode_2:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution_2_V2:
    def maxDepth(self, node: Optional[TreeNode_2]) -> int:
        if not node:
            return 0
        return 1 + max(self.maxDepth(node.left), self.maxDepth(node.right))

# ============================================================================
# Solution 3: A    (原文件: 05 - 0104 - A - Max Depth Binary Tree - Recursive.py)
# ============================================================================

class Solution_3_A:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0
            return 1 + max(dfs(node.left), dfs(node.right))
        return dfs(root)

# ============================================================================
# Solution 4: B    (原文件: 05 - 0104 - B - Max Depth Binary Tree - Recursive.py)
# ============================================================================

class Solution_4_B:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        depth = 0
        queue = deque([root])
        while queue:
            for _ in range(len(queue)):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            depth += 1
        return depth
