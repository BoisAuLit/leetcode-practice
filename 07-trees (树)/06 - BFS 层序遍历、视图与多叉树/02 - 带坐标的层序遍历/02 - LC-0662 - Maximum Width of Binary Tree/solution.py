"""LC-0662 - Maximum Width of Binary Tree（第二轮自主新增）

Level 1 · 06 BFS 层序遍历、视图与多叉树 —— 给节点编**堆式下标**
题目在问：每层的宽度 = 该层**最左和最右非空节点之间的距离**（中间的 None 也算进长度），
         求所有层中的最大宽度。

为什么新增它（补什么缺口）：
  本 Level 2 原本只有 LC-0314（按**列坐标**分组）。本题引入另一种坐标：
  **堆式编号** `root = 0, left = 2i+1, right = 2i+2`（或 `2i` / `2i+1`）。
  这个编号让「两个节点之间隔了多少个位置」变成一次减法，
  是「把树映射到数组下标」这一类技巧（堆、线段树、完全二叉树）的入门。
  LC-0314 回答「在哪一列」，本题回答「在这一层的第几个位置」—— 两者互补。

决定性观察：
  1. 给每个节点一个编号 `i`，左孩子 `2i+1`，右孩子 `2i+2`。
     这样**同一层的编号是连续的**（即使中间节点缺失，编号也会留出空位）。
  2. 每层宽度 = `该层最后一个节点的编号 - 第一个节点的编号 + 1`。
  3. **编号会指数级增长**（深度 60 就超过 2^60）。
     Python 整数无上限不会溢出，但在 C++/Java 里必须处理。
     通用做法：**每层把编号减去该层第一个节点的编号**，让编号从 0 重新开始。
     本实现做了这个归一化，既安全又能直接迁移到别的语言。

**为什么不能只数每层的节点个数**：题目算的是「最左到最右的跨度」，
      中间的空位也要计入。`[1,3,2,5,3,null,9]` 最后一层只有 4 个节点，
      但宽度是 4；而 `[1,3,2,5,null,null,9]` 最后一层只有 2 个节点，宽度却是 4。

复杂度：O(n) 时间，O(w) 空间。

边界：
  - 单节点 → 1
  - 一条左链 / 右链 → 每层宽度都是 1
  - 完全二叉树 → 最后一层最宽
  - 深度很大的稀疏树（验证编号归一化）
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

from collections import deque


##################################################################################################
##### ! Solution 1: BFS + 堆式编号 + 每层归一化（防止编号爆炸）
##### ! 时间复杂度: O(n)   空间复杂度: O(w)
##### ! 适用：所有「节点在本层的第几个位置」类问题；归一化是跨语言安全的关键
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        best = 0
        queue = deque([(root, 0)])
        while queue:
            base = queue[0][1]            # ! 本层第一个节点的编号，用来归一化
            size = len(queue)
            first = last = 0
            for k in range(size):
                node, idx = queue.popleft()
                idx -= base               # ! 归一化：让本层编号从 0 开始，避免指数级增长
                if k == 0:
                    first = idx
                last = idx
                if node.left:
                    queue.append((node.left, 2 * idx + 1))
                if node.right:
                    queue.append((node.right, 2 * idx + 2))
            best = max(best, last - first + 1)
        return best


##################################################################################################
##### ! Solution 2: DFS 记录每层最左编号，再用当前编号作差
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：想用 DFS 做分层统计时；注意必须先走左子树才能保证 first 记的是最左
##################################################################################################


class Solution_2:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        first: dict[int, int] = {}        # ! depth -> 该层最左节点的编号
        self.best = 0

        def dfs(node, depth, idx):
            if not node:
                return
            if depth not in first:
                first[depth] = idx        # ! 先走左子树，所以第一次写入的就是最左
            self.best = max(self.best, idx - first[depth] + 1)
            dfs(node.left, depth + 1, 2 * idx)
            dfs(node.right, depth + 1, 2 * idx + 1)

        dfs(root, 0, 0)
        return self.best


if __name__ == "__main__":
    import random

    cases = [([1, 3, 2, 5, 3, None, 9], 4), ([1, 3, 2, 5, None, None, 9], 4),
             ([1, 3, None, 5, 3], 2), ([1], 1), ([1, 1], 1),
             ([1, 1, 1, 1, None, None, 1, 1, None, None, 1], 8)]
    for vals, _ in cases:
        a = Solution_1().widthOfBinaryTree(TreeNode.from_list(vals))
        b = Solution_2().widthOfBinaryTree(TreeNode.from_list(vals))
        assert a == b, (vals, a, b)
        print(f"{vals} -> {a}")

    for _ in range(800):
        vals = [random.choice([1, 1, None]) for _ in range(random.randint(1, 20))]
        vals[0] = 1
        a = Solution_1().widthOfBinaryTree(TreeNode.from_list(vals))
        b = Solution_2().widthOfBinaryTree(TreeNode.from_list(vals))
        assert a == b, (vals, a, b)
    print("随机对拍 800 组通过 ✓（BFS 归一化编号 == DFS 最左编号作差）")
