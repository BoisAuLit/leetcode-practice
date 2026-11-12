"""LC-0437 - Path Sum III

Level 1 · 03 路径 DFS、状态传递与 Prefix Sum —— **数组前缀和技巧迁移到树上**
题目在问：统计路径和等于 targetSum 的路径数量。
         路径可以从**任意节点**开始、任意节点结束，但**必须沿父→子方向向下**。

这是本章最有价值的一道题：它把「数组里用前缀和 + 哈希表数子数组」整套搬到了树上。

决定性观察：
  1. 「从任意祖先开始、向下结束」= 在**一条根到当前节点的链**上，找一段后缀和等于 target。
     链上的问题 ⟹ 和数组子数组问题同构。
  2. 设 `s` = 从 root 到当前节点的前缀和。
     若存在某个祖先的前缀和 `s - targetSum`，那么从那个祖先的**下一个节点**到当前节点
     这一段的和就是 targetSum。所以：
        `答案 += prefix_count[s - targetSum]`
  3. `prefix_count` 统计的是**当前这条根到节点的链上**出现过的前缀和。

三个关键细节（全是坑）：
  - **`prefix_count[0] = 1` 必须初始化**：表示「空前缀」，
    它代表「这条路径从 root 本身开始」的情况。不初始化会漏掉所有从根开始的答案。
  - **返回时必须撤销**：`prefix_count[s] -= 1`。
    否则左子树的前缀和会被右子树看到 —— 但它们**不在同一条根到节点的链上**，
    不构成合法路径。这就是「不同分支的前缀和不能混」。
  - 统计要**先查后加**还是**先加后查**？本实现是「先把当前 s 查完再把 s 记进去」
    的顺序更安全吗？其实这里 `s` 自己也要记入，供**子孙**使用；
    当前节点自己查的是**祖先们**的前缀和。代码里先 `res += cnt[s - target]`
    再 `cnt[s] += 1`，顺序保证了不会把自己算成自己的祖先。
    （若 target == 0，顺序写反会多算一条长度为 0 的「路径」。）

**为什么不能用滑动窗口**：节点值可以是**负数**，
      前缀和沿路径不单调，「和太大就收缩左端」的前提不成立。
      这和 LC-0862（数组含负数时不能用普通滑窗）是同一个道理。

复杂度：**O(n) 期望**（每个节点一次哈希查询），O(h) 空间。
      朴素做法「以每个节点为起点各跑一次 DFS」是 O(n²)（链状树）或 O(n log n)（平衡树）。

边界：
  - 空树 → 0
  - 负数节点值 / 负的 targetSum
  - targetSum == 0（需要小心上面说的顺序问题）
  - 同一条路径被多次计数（不同起点算不同路径）
  - 单节点等于 target
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
##### ! Solution 1: 树上前缀和 + 哈希计数 + 回溯撤销
##### ! 时间复杂度: O(n) 期望   空间复杂度: O(h)
##### ! 适用：树上「任意起点向下的路径计数」；数组前缀和技巧的树上版本
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


from collections import defaultdict


class Solution_1:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        count = defaultdict(int)
        count[0] = 1                      # ! 空前缀：代表「路径从 root 开始」
        self.res = 0

        def dfs(node, s):
            if not node:
                return
            s += node.val
            self.res += count[s - targetSum]   # ! 先查祖先，避免把自己当成自己的祖先
            count[s] += 1                      # ! 再把自己记进去，供子孙使用
            dfs(node.left, s)
            dfs(node.right, s)
            count[s] -= 1                      # ! 回溯：离开这条链就撤销，不污染兄弟分支

        dfs(root, 0)
        return self.res


##################################################################################################
##### ! Solution 2: 朴素双层 DFS —— 以每个节点为起点各数一次
##### ! 时间复杂度: O(n^2) 最坏（链状树），平衡树 O(n log n)   空间复杂度: O(h)
##### ! 适用：面试先给这版再优化成 Solution_1；逻辑最直白，不容易错
##################################################################################################


class Solution_2:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        def count_from(node, remain):
            """以 node 为路径起点，向下有多少条和为 remain 的路径。"""
            if not node:
                return 0
            remain -= node.val
            hit = 1 if remain == 0 else 0      # ! 注意不能在这里 return，负数时后面还可能凑回来
            return hit + count_from(node.left, remain) + count_from(node.right, remain)

        def dfs(node):
            if not node:
                return 0
            return count_from(node, targetSum) + dfs(node.left) + dfs(node.right)

        return dfs(root)


if __name__ == "__main__":
    import random

    cases = [([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1], 8),
             ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22),
             ([], 0), ([1], 1), ([1], 0), ([0, 1, 1], 1), ([1, -2, -3], -1)]
    for vals, t in cases:
        a = Solution_1().pathSum(TreeNode.from_list(vals), t)
        b = Solution_2().pathSum(TreeNode.from_list(vals), t)
        assert a == b, (vals, t, a, b)
        print(f"{vals}, target={t} -> {a}")

    for _ in range(1000):                # ! 含负数和 target=0 的随机对拍
        vals = [random.choice([random.randint(-3, 3), None]) for _ in range(random.randint(0, 11))]
        if vals and vals[0] is None:
            vals[0] = 0
        t = random.randint(-4, 4)
        a = Solution_1().pathSum(TreeNode.from_list(vals), t)
        b = Solution_2().pathSum(TreeNode.from_list(vals), t)
        assert a == b, (vals, t, a, b)
    print("随机对拍 1000 组通过 ✓（含负数与 target=0）")
