"""LC-0938 - Range Sum of BST（第二轮自主新增）

Level 1 · 04 BST 有序性质与操作 —— 用 BST 不变量做**剪枝（Pruning）**
题目在问：求 BST 中所有值落在 `[low, high]` 内的节点之和。

为什么新增它（它补的是哪个缺口）：
  LC-0700 用 BST 不变量**定位一个值**；本题用同一个不变量**裁剪整棵子树**。
  这是 BST 最实用的一个思维升级：
  **「这棵子树里的值全都超出范围了 ⟹ 整棵不用进」**。
  同样的剪枝直接迁移到 LC-0669 Trim a BST、LC-0230 Kth Smallest 的提前退出等。
  成本几乎为零，收益是一个能复用的剪枝直觉。

决定性观察：
  1. `node.val < low` ⟹ **整棵左子树都 < low**，全部无用 ⟹ 只递归右子树。
  2. `node.val > high` ⟹ **整棵右子树都 > high** ⟹ 只递归左子树。
  3. 否则当前节点在范围内，计入答案，**两边都要递归**
     （左边可能还有 ≥ low 的，右边可能还有 ≤ high 的）。

**不剪枝会怎样**：退化成遍历整棵树 O(n)。剪枝之后，
      只会访问「范围内的节点」+「到范围边界路径上的节点」，实际快很多。
      但**最坏仍是 O(n)**（范围覆盖整棵树时），所以不要说成 O(log n)。

复杂度：O(n) 最坏，实际 O(范围内节点数 + h)；空间 O(h)。

边界：
  - 范围覆盖全树 → 所有节点和
  - 范围不含任何节点 → 0
  - low == high（只取一个值）
  - 空树 → 0
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
    @staticmethod
    def build_bst(values):
        """按插入顺序建一棵 BST（测试用）。"""
        root = None

        def insert(node, v):
            if not node:
                return TreeNode(v)
            if v < node.val:
                node.left = insert(node.left, v)
            elif v > node.val:
                node.right = insert(node.right, v)
            return node

        for v in values:
            root = insert(root, v)
        return root

    @staticmethod
    def inorder(root):
        out, stack, cur = [], [], root
        while stack or cur:
            while cur:
                stack.append(cur); cur = cur.left
            cur = stack.pop(); out.append(cur.val); cur = cur.right
        return out

    @staticmethod
    def is_bst(root):
        vals = TreeNode.inorder(root)
        return all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))


##################################################################################################
##### ! Solution 1: 递归 + BST 剪枝（范围外的整棵子树直接不进）
##### ! 时间复杂度: O(n) 最坏，实际 O(范围内节点数 + h)   空间复杂度: O(h)
##### ! 适用：BST 上的区间查询 / 区间裁剪；LC-0669 用的是同一个剪枝
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if not root:
            return 0
        if root.val < low:                                   # ! 左子树整棵都 < low，剪掉
            return self.rangeSumBST(root.right, low, high)
        if root.val > high:                                  # ! 右子树整棵都 > high，剪掉
            return self.rangeSumBST(root.left, low, high)
        return (root.val
                + self.rangeSumBST(root.left, low, high)
                + self.rangeSumBST(root.right, low, high))


##################################################################################################
##### ! Solution 2: 迭代 DFS + 同样的剪枝（显式栈，避免递归深度问题）
##### ! 时间复杂度: 同上   空间复杂度: O(h)
##### ! 适用：树可能很深时
##################################################################################################


class Solution_2:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        total, stack = 0, [root]
        while stack:
            node = stack.pop()
            if not node:
                continue
            if node.val < low:
                stack.append(node.right)
            elif node.val > high:
                stack.append(node.left)
            else:
                total += node.val
                stack.append(node.left)
                stack.append(node.right)
        return total


##################################################################################################
##### ! Solution 3: 遍历整棵树逐个判断（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：正确性参照 —— 它完全没利用 BST 性质，正好用来证明剪枝没剪错
##################################################################################################


class Solution_3:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if not root:
            return 0
        cur = root.val if low <= root.val <= high else 0
        return cur + self.rangeSumBST(root.left, low, high) + self.rangeSumBST(root.right, low, high)


if __name__ == "__main__":
    import random

    cases = [([10, 5, 15, 3, 7, None, 18], 7, 15), ([10, 5, 15, 3, 7, 13, 18, 1, None, 6], 6, 10),
             ([], 0, 10), ([5], 5, 5), ([5], 6, 10)]
    for vals, lo, hi in cases:
        r = TreeNode.from_list(vals)
        a = Solution_1().rangeSumBST(r, lo, hi)
        b = Solution_2().rangeSumBST(r, lo, hi)
        c = Solution_3().rangeSumBST(r, lo, hi)
        assert a == b == c, (vals, lo, hi, a, b, c)
        print(f"{vals}, [{lo},{hi}] -> {a}")

    for _ in range(800):                 # ! 随机 BST 对拍：剪枝版必须和全遍历版完全一致
        vals = random.sample(range(0, 40), random.randint(0, 14))
        r = TreeNode.build_bst(vals)
        lo = random.randint(-2, 40); hi = lo + random.randint(0, 20)
        a = Solution_1().rangeSumBST(r, lo, hi)
        b = Solution_2().rangeSumBST(r, lo, hi)
        c = Solution_3().rangeSumBST(r, lo, hi)
        assert a == b == c, (vals, lo, hi, a, b, c)
    print("随机对拍 800 组通过 ✓（剪枝 == 全遍历）")
