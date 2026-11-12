"""LC-0450 - Delete Node in a BST

Level 1 · 04 BST 有序性质与操作 —— BST 删除的**三种情况**
题目在问：从 BST 中删除值为 key 的节点，返回新的根，且**删完仍是合法 BST**。

为什么删除比插入难（和 LC-0701 对照）：
  插入永远能挂在一个**叶子位置**，不动已有结构。
  删除却可能挖掉一个**有两个孩子的内部节点** —— 两个孩子只能有一个顶上来，
  必须找一个「正好能替代它位置」的值。

决定性观察 —— 三种情况：
  1. **叶节点**（无孩子）：直接删掉，返回 None。
  2. **只有一个孩子**：让那个孩子顶上去，返回它。
  3. **两个孩子**（关键情况）：找一个**替身**：
     - **Inorder Successor（中序后继）**= 右子树里**最小**的节点，或者
     - **Inorder Predecessor（中序前驱）**= 左子树里**最大**的节点。
     把替身的值复制到当前节点，然后**递归地在对应子树里删掉那个替身**。

**为什么替身一定可行**：中序后继是「所有大于当前节点的值里最小的那个」。
     把它放到当前位置，左子树全都还比它小、右子树（去掉它之后）全都还比它大，
     **BST 不变量完整保持**。换成中序前驱同理（对称）。

**为什么递归删替身不会无限下去**：中序后继是右子树的最左节点，
     它**必然没有左孩子**，所以落到情况 1 或 2，一步就结束。

统一的返回值契约：`delete(node, key)` 返回「删除后这棵子树的新根」，
     父亲用 `node.left = delete(node.left, key)` 重新接线。
     这个套路和 LC-0701 的递归版完全一致 —— **「返回新子树根」是 BST 修改类题的通用骨架**。

复杂度：O(h) 时间（找节点 O(h) + 找替身 O(h)），O(h) 空间（递归栈）。

边界：
  - key 不存在 → 原样返回
  - 删除根节点
  - 删除叶子 / 只有左孩子 / 只有右孩子 / 两个孩子
  - 空树
  - 删完变成空树
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
##### ! Solution 1: 递归 + 三种情况 + 中序后继（右子树最小）当替身
##### ! 时间复杂度: O(h)   空间复杂度: O(h)
##### ! 适用：BST 删除的标准答案；「返回新子树根」的契约是 BST 修改题的通用骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return None                              # ! key 不存在
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if not root.left:                        # ! 情况 1/2：没有左孩子 → 右孩子顶上（可能是 None）
                return root.right
            if not root.right:                       # ! 情况 2：没有右孩子 → 左孩子顶上
                return root.left
            succ = root.right                        # ! 情况 3：中序后继 = 右子树的最左节点
            while succ.left:
                succ = succ.left
            root.val = succ.val                      # ! 用替身的值覆盖当前节点
            root.right = self.deleteNode(root.right, succ.val)   # ! 再去右子树把替身删掉（它没有左孩子，一步到位）
        return root


##################################################################################################
##### ! Solution 2: 用中序**前驱**（左子树最大）当替身 —— 对称写法
##### ! 时间复杂度: O(h)   空间复杂度: O(h)
##### ! 适用：说明替身的选择不唯一；两种都能保持 BST 不变量
##################################################################################################


class Solution_2:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return None
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if not root.right:
                return root.left
            if not root.left:
                return root.right
            pred = root.left                         # ! 中序前驱 = 左子树的最右节点
            while pred.right:
                pred = pred.right
            root.val = pred.val
            root.left = self.deleteNode(root.left, pred.val)
        return root


##################################################################################################
##### ! Solution 3: 取出中序序列、去掉 key、重建 BST（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 它保证结果一定是合法 BST，用来验证上面两种替身法
##################################################################################################


class Solution_3:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        vals = [v for v in TreeNode.inorder(root) if v != key]

        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            node = TreeNode(vals[mid])
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node

        return build(0, len(vals) - 1)


if __name__ == "__main__":
    import random

    r = TreeNode.from_list([5, 3, 6, 2, 4, None, 7])
    print("删 3 ->", TreeNode.inorder(Solution_1().deleteNode(r, 3)))

    for _ in range(1000):                # ! 随机对拍：两种替身法都必须得到合法 BST 且中序一致
        vals = random.sample(range(0, 30), random.randint(0, 12))
        key = random.randint(-1, 31)
        expect = sorted(v for v in vals if v != key)
        r1 = Solution_1().deleteNode(TreeNode.build_bst(vals), key)
        r2 = Solution_2().deleteNode(TreeNode.build_bst(vals), key)
        r3 = Solution_3().deleteNode(TreeNode.build_bst(vals), key)
        for name, r in (("后继法", r1), ("前驱法", r2), ("重建法", r3)):
            assert TreeNode.inorder(r) == expect, (name, vals, key, TreeNode.inorder(r), expect)
            assert TreeNode.is_bst(r), (name, vals, key)
    print("随机对拍 1000 组通过 ✓（中序后继法 / 中序前驱法 / 重建法三者一致，且都是合法 BST）")
