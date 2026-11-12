"""LC-0103 - Binary Tree Zigzag Level Order Traversal

Level 1 · 06 BFS 层序遍历、视图与多叉树 —— 在标准 BFS 上加一个方向开关
题目在问：层序遍历，但**奇数层从左到右、偶数层从右到左**交替输出。

决定性观察：
  1. **BFS 的遍历顺序完全不用改。** 改的只是「每一层的结果怎么摆」。
     最干净的做法：照常 BFS，收完一层之后，如果该层需要反向就 `level[::-1]`。
  2. **不要试图通过交替改变入队顺序来实现** —— 那会把下一层的父子对应关系搞乱，
     是这道题最常见的错误思路。
  3. 「每层多少个节点」靠 `for _ in range(len(queue))` 在进入该层时**先固定住**。
     这是所有分层 BFS 的通用写法。

两种实现的取舍：
  - **翻转法**：`level[::-1]`，O(层宽) 的额外拷贝，代码最短最不易错。
  - **双端队列法**：用 `deque`，正向层 `append`、反向层 `appendleft`，
    省掉一次反转。严格来说更优，但差别只是常数。

复杂度：O(n) 时间，O(w) 空间（w 是最大层宽）。

和同 Level 2 另外两题的关系：
  - **LC-0102** 标准层序 —— 本题的基础。
  - **LC-0199 右视图** —— 每层只取最后一个。
  三道题共用同一个「分层 BFS」骨架，**区别只在收集这一层结果的方式**：
  102 全要、103 交替反转、199 只要最后一个。

边界：
  - 空树 → []
  - 单节点 → [[root]]
  - 只有左链 / 只有右链
  - 第 0 层（根）永远是从左到右
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
##### ! Solution 1: 标准分层 BFS + 按层号决定是否反转
##### ! 时间复杂度: O(n)   空间复杂度: O(w)
##### ! 适用：所有「层序 + 每层做点加工」的题；改一行就是 102 / 199
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        res, queue, left_to_right = [], deque([root]), True
        while queue:
            level = []
            for _ in range(len(queue)):      # ! 进层时先固定住这一层的节点数
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            res.append(level if left_to_right else level[::-1])   # ! 只改「怎么摆」，不改遍历顺序
            left_to_right = not left_to_right
        return res


##################################################################################################
##### ! Solution 2: 用 deque 装每层结果，反向层用 appendleft（省掉一次反转）
##### ! 时间复杂度: O(n)   空间复杂度: O(w)
##### ! 适用：想省掉 [::-1] 的拷贝时；本质完全相同
##################################################################################################


class Solution_2:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        res, queue, ltr = [], deque([root]), True
        while queue:
            level = deque()
            for _ in range(len(queue)):
                node = queue.popleft()
                if ltr:
                    level.append(node.val)
                else:
                    level.appendleft(node.val)    # ! 反向层直接从左边塞
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            res.append(list(level))
            ltr = not ltr
        return res


##################################################################################################
##### ! Solution 3: DFS 按深度分桶，最后统一反转奇数层（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：正确性参照；也说明「层序结果」不一定非要用 BFS 才能拿到
##################################################################################################


class Solution_3:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        levels: List[List[int]] = []

        def dfs(node, d):
            if not node:
                return
            if d == len(levels):
                levels.append([])
            levels[d].append(node.val)
            dfs(node.left, d + 1)
            dfs(node.right, d + 1)

        dfs(root, 0)
        return [lv if i % 2 == 0 else lv[::-1] for i, lv in enumerate(levels)]


if __name__ == "__main__":
    import random

    cases = [[3, 9, 20, None, None, 15, 7], [1], [], [1, 2, 3, 4, 5, 6, 7],
             [1, 2, None, 3, None, 4], [1, None, 2, None, 3]]
    for vals in cases:
        a = Solution_1().zigzagLevelOrder(TreeNode.from_list(vals))
        b = Solution_2().zigzagLevelOrder(TreeNode.from_list(vals))
        c = Solution_3().zigzagLevelOrder(TreeNode.from_list(vals))
        assert a == b == c, (vals, a, b, c)
        print(f"{vals} -> {a}")

    for _ in range(800):
        vals = [random.choice([random.randint(0, 9), None]) for _ in range(random.randint(0, 14))]
        if vals and vals[0] is None:
            vals[0] = 1
        a = Solution_1().zigzagLevelOrder(TreeNode.from_list(vals))
        b = Solution_2().zigzagLevelOrder(TreeNode.from_list(vals))
        c = Solution_3().zigzagLevelOrder(TreeNode.from_list(vals))
        assert a == b == c, (vals, a, b, c)
    print("随机对拍 800 组通过 ✓")
