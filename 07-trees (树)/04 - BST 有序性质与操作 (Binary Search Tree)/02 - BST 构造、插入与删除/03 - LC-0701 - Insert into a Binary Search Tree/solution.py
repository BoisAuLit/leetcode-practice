"""LC-0701 - Insert into a Binary Search Tree（第二轮自主新增）

Level 1 · 04 BST 有序性质与操作 —— 和 LC-0450 组成 BST 的「增删」一对
题目在问：往 BST 里插入一个值（保证原树中不存在），返回插入后的根。

为什么新增它：
  本章原本有「查」（0700）、「验证」（0098）、「删」（0450），**唯独缺「插」**。
  插入是三者中最简单的，但它是**理解删除为什么难**的前提：
  插入永远可以挂在一个**叶子**位置上，不需要重排任何已有结构；
  删除却可能挖掉一个有两个孩子的内部节点，必须找替身。
  把两题放在一起，BST 的 CRUD 就完整了，而成本只有几行代码。

决定性观察：
  1. 沿 BST 不变量一路往下走，**走到空位就是插入点**。
     不需要旋转、不需要平衡（题目不要求保持平衡）。
  2. **新节点一定是叶子**。这是插入和删除最大的区别。
  3. 插入位置不唯一（题目明确说任何合法 BST 都接受），
     但「走到底挂叶子」是最简单、也最常被接受的那一种。

复杂度：O(h) 时间（平衡 O(log n)，退化 O(n)），
      迭代版 O(1) 空间，递归版 O(h) 栈。

**注意不保证平衡**：按升序依次插入 1..n，会得到一条长度 n 的链，
      之后所有操作退化成 O(n)。真实场景要用 AVL / 红黑树，
      但那不在本题范围 —— 面试提一句即可。

边界：
  - 空树 → 新节点成为根
  - 插入值比所有节点都小 / 都大 → 挂在最左 / 最右
  - 退化成链的 BST
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
##### ! Solution 1: 迭代 —— 沿 BST 不变量往下走，空位就是插入点
##### ! 时间复杂度: O(h)   空间复杂度: O(1)
##### ! 适用：BST 插入的默认写法；新节点一定是叶子
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        node = TreeNode(val)
        if not root:
            return node
        cur = root
        while True:
            if val < cur.val:
                if not cur.left:
                    cur.left = node
                    return root
                cur = cur.left
            else:
                if not cur.right:
                    cur.right = node
                    return root
                cur = cur.right


##################################################################################################
##### ! Solution 2: 递归 —— 「返回插入后的子树根」是最干净的写法
##### ! 时间复杂度: O(h)   空间复杂度: O(h) 栈
##### ! 适用：这个「返回新子树根并让父亲重新接线」的套路，正是 LC-0450 删除用的同一招
##################################################################################################


class Solution_2:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return TreeNode(val)              # ! 空位 → 新节点
        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)    # ! 让父亲重新接上返回值
        else:
            root.right = self.insertIntoBST(root.right, val)
        return root


if __name__ == "__main__":
    import random

    r = TreeNode.from_list([4, 2, 7, 1, 3])
    out = TreeNode.to_list(Solution_1().insertIntoBST(r, 5))
    print("插入 5 ->", out)
    assert TreeNode.is_bst(TreeNode.from_list(out))

    for _ in range(800):                 # ! 随机对拍：两种写法都必须得到合法 BST 且中序序列一致
        vals = random.sample(range(0, 40), random.randint(0, 12))
        new = random.choice([v for v in range(0, 40) if v not in vals])
        t1 = TreeNode.build_bst(vals)
        t2 = TreeNode.build_bst(vals)
        r1 = Solution_1().insertIntoBST(t1, new)
        r2 = Solution_2().insertIntoBST(t2, new)
        i1, i2 = TreeNode.inorder(r1), TreeNode.inorder(r2)
        assert i1 == i2 == sorted(vals + [new]), (vals, new, i1, i2)
        assert TreeNode.is_bst(r1) and TreeNode.is_bst(r2), (vals, new)
    print("随机对拍 800 组通过 ✓（插入后仍是合法 BST，中序 == 排序后的全集）")
