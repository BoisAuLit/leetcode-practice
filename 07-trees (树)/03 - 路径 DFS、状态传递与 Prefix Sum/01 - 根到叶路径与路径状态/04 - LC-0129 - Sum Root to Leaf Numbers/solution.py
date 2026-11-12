"""LC-0129 - Sum Root to Leaf Numbers

Level 1 · 03 路径 DFS、状态传递与 Prefix Sum —— Top-down 状态传递（把路径压成一个数）
题目在问：每条根到叶的路径组成一个十进制数（根是最高位），求所有这些数的和。

决定性观察：
  1. **不需要保存整条路径**。沿路只要维护一个数字：
        `cur = cur * 10 + node.val`
     这就是「把路径状态压缩成一个标量」—— 比 LC-0113 存列表便宜得多。
  2. 这个状态是**自顶向下（Top-down）传递**的：父亲算好了再交给孩子。
     与之相对，LC-0124 / LC-0543 是**自底向上（Bottom-up）汇总**。
     本章要的就是分清这两个方向。
  3. 只在**叶节点**结算（`not node.left and not node.right`）。
     在 None 处结算会导致单侧孩子的节点被算两次。

**为什么不需要回溯**：`cur` 是按值传参的整数，每次递归都是一个新的局部变量，
      天然隔离了兄弟分支。只有当状态是**可变对象**（列表、集合）时才需要显式回溯。
      这个对比值得和 LC-0113 放在一起记。

四道 Top-down 路径题的状态对照（本 Level 2 的全部内容）：

| 题 | 向下传什么 | 什么时候结算 |
|---|---|---|
| LC-0112 Path Sum | 剩余 target（标量） | 叶节点，判 `remain == 0` |
| LC-0113 Path Sum II | 剩余 target + **路径列表**（可变 ⟹ 要回溯） | 叶节点，拷贝路径 |
| LC-0257 Binary Tree Paths | 路径字符串（不可变 ⟹ 不用回溯） | 叶节点 |
| LC-0129 本题 | 当前数字（标量） | 叶节点，累加 |

复杂度：O(n) 时间，O(h) 空间（递归栈）。

边界：
  - 空树 → 0
  - 单节点 [5] → 5
  - [1,2,3] → 12 + 13 = 25
  - [4,9,0,5,1] → 495 + 491 + 40 = 1026
  - 节点值含 0（[1,0] → 10）
"""

from typing import List, Optional


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
        queue, i = [root], 1
        while queue and i < len(values):
            node = queue.pop(0)
            if i < len(values):
                if values[i] is not None:
                    node.left = TreeNode(values[i]); queue.append(node.left)
                i += 1
            if i < len(values):
                if values[i] is not None:
                    node.right = TreeNode(values[i]); queue.append(node.right)
                i += 1
        return root

    @staticmethod
    def to_list(root):
        if not root:
            return []
        out, queue = [], [root]
        while queue:
            node = queue.pop(0)
            if node:
                out.append(node.val); queue.append(node.left); queue.append(node.right)
            else:
                out.append(None)
        while out and out[-1] is None:
            out.pop()
        return out

##################################################################################################
##### ! Solution 1: Top-down DFS，沿路维护 cur = cur*10 + node.val
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：所有「把根到叶路径压缩成一个标量状态」的题；不需要回溯
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        def dfs(node, cur):
            if not node:
                return 0
            cur = cur * 10 + node.val
            if not node.left and not node.right:     # ! 只在叶节点结算
                return cur
            return dfs(node.left, cur) + dfs(node.right, cur)

        return dfs(root, 0)


##################################################################################################
##### ! Solution 2: 迭代 DFS（显式栈携带状态）
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：被要求「不用递归」时；展示「递归状态 == 栈里存的元组」
##################################################################################################


class Solution_2:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        total = 0
        stack = [(root, 0)]
        while stack:
            node, cur = stack.pop()
            cur = cur * 10 + node.val
            if not node.left and not node.right:
                total += cur
                continue
            if node.right:
                stack.append((node.right, cur))
            if node.left:
                stack.append((node.left, cur))
        return total


##################################################################################################
##### ! Solution 3: 先收集所有根到叶路径再转成数字（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2) 最坏   空间复杂度: O(n^2)
##### ! 适用：正确性参照；也最直白地表达题面定义
##################################################################################################


class Solution_3:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        paths: List[str] = []

        def dfs(node, s):
            if not node:
                return
            s = s + str(node.val)
            if not node.left and not node.right:
                paths.append(s)
                return
            dfs(node.left, s)
            dfs(node.right, s)

        dfs(root, "")
        return sum(int(p) for p in paths)


if __name__ == "__main__":
    import random

    cases = [[1, 2, 3], [4, 9, 0, 5, 1], [], [5], [1, 0], [1, 2, 3, 4, 5, 6, 7]]
    for vals in cases:
        a = Solution_1().sumNumbers(TreeNode.from_list(vals))
        b = Solution_2().sumNumbers(TreeNode.from_list(vals))
        c = Solution_3().sumNumbers(TreeNode.from_list(vals))
        assert a == b == c, (vals, a, b, c)
        print(f"{vals} -> {a}")

    for _ in range(500):
        vals = [random.choice([random.randint(0, 9), None]) for _ in range(random.randint(0, 10))]
        if vals and vals[0] is None:
            vals[0] = 1
        a = Solution_1().sumNumbers(TreeNode.from_list(vals))
        b = Solution_2().sumNumbers(TreeNode.from_list(vals))
        c = Solution_3().sumNumbers(TreeNode.from_list(vals))
        assert a == b == c, (vals, a, b, c)
    print("随机对拍 500 组通过 ✓")
