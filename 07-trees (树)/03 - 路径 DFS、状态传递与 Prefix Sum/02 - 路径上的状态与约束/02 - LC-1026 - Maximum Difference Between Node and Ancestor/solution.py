"""LC-1026 - Maximum Difference Between Node and Ancestor（第二轮自主新增）

Level 1 · 03 路径 DFS、状态传递与 Prefix Sum —— Top-down 同时传递 **min 和 max**
题目在问：求 `|a.val - b.val|` 的最大值，其中 a 是 b 的祖先。

为什么新增它（和 LC-1448 的关系）：
  LC-1448 Count Good Nodes 沿路向下传**一个**状态（路径最大值）。
  本题要传**两个**（路径最小值和最大值），而且目标从「计数」变成「取最值」。
  两题并排，就能把「Top-down 状态传递」从「传一个标量」推广到「传一组标量」，
  成本极低、迁移性高。它也是 LeetCode 高频的 Easy-Medium 题。

决定性观察：
  1. 对一条根到当前节点的路径，**最优的祖先一定是路径上的最大值或最小值**。
     因为 `|cur - ancestor|` 要最大，ancestor 当然取极端的那个。
  2. 所以沿路只要维护 `(lo, hi)` = 到当前节点为止路径上的最小值和最大值，
     在每个节点更新答案：`ans = max(ans, hi - lo)`。
  3. **在哪里结算？** 在每个节点（包括内部节点）都结算，不只在叶子。
     不过只在叶子结算也对 —— 因为 `hi - lo` 沿路**单调不减**，叶子处必然最大。
     本实现在叶子结算，顺便说明这个单调性。

为什么不用回溯：`lo` / `hi` 是按值传递的整数，每层都是新的局部变量，
      兄弟分支天然隔离（和 LC-0129 同理）。

复杂度：O(n) 时间，O(h) 空间。

边界：
  - 单节点 → 0（没有祖先-后代对）
  - 一条链递增 → 根与最深叶的差
  - 全部相等 → 0
  - 含负数
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
##### ! Solution 1: Top-down 传 (lo, hi)，在叶子结算 hi - lo
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：「祖先-后代之间的极值关系」类题；LC-1448 的双状态版本
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        def dfs(node, lo, hi):
            if not node:
                return hi - lo            # ! hi-lo 沿路单调不减，到底了直接结算
            lo = min(lo, node.val)
            hi = max(hi, node.val)
            return max(dfs(node.left, lo, hi), dfs(node.right, lo, hi))

        return dfs(root, root.val, root.val)


##################################################################################################
##### ! Solution 2: 每个节点都结算（不依赖「单调不减」这个性质，更保险）
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：当目标函数不再单调时（比如换成别的组合方式），这版还能用
##################################################################################################


class Solution_2:
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:
        self.ans = 0

        def dfs(node, lo, hi):
            if not node:
                return
            self.ans = max(self.ans, abs(node.val - lo), abs(node.val - hi))
            lo = min(lo, node.val)
            hi = max(hi, node.val)
            dfs(node.left, lo, hi)
            dfs(node.right, lo, hi)

        if root:
            dfs(root, root.val, root.val)
        return self.ans


##################################################################################################
##### ! Solution 3: 暴力枚举所有 (祖先, 后代) 对（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2) 最坏   空间复杂度: O(h)
##### ! 适用：正确性参照 —— 直接按题面定义枚举
##################################################################################################


class Solution_3:
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:
        best = 0

        def desc(node, ancestor_val):
            nonlocal best
            if not node:
                return
            best = max(best, abs(ancestor_val - node.val))
            desc(node.left, ancestor_val)
            desc(node.right, ancestor_val)

        def walk(node):
            if not node:
                return
            desc(node.left, node.val)
            desc(node.right, node.val)
            walk(node.left)
            walk(node.right)

        walk(root)
        return best


if __name__ == "__main__":
    import random

    cases = [[8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], [1, None, 2, None, 0, 3],
             [5], [], [1, 2, 3], [-1, -2, -3]]
    for vals in cases:
        a = Solution_1().maxAncestorDiff(TreeNode.from_list(vals))
        b = Solution_2().maxAncestorDiff(TreeNode.from_list(vals))
        c = Solution_3().maxAncestorDiff(TreeNode.from_list(vals))
        assert a == b == c, (vals, a, b, c)
        print(f"{vals} -> {a}")

    for _ in range(500):
        vals = [random.choice([random.randint(-5, 9), None]) for _ in range(random.randint(0, 10))]
        if vals and vals[0] is None:
            vals[0] = 1
        a = Solution_1().maxAncestorDiff(TreeNode.from_list(vals))
        b = Solution_2().maxAncestorDiff(TreeNode.from_list(vals))
        c = Solution_3().maxAncestorDiff(TreeNode.from_list(vals))
        assert a == b == c, (vals, a, b, c)
    print("随机对拍 500 组通过 ✓")
