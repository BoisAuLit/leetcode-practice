"""LC-0700 - Search in a Binary Search Tree

Level 1 · 04 BST 有序性质与操作 —— BST 不变量的最基础应用
题目在问：在 BST 中找值为 val 的子树根，找不到返回 None。

决定性观察（整个 BST 章节的地基）：
  **BST 不变量**：对任意节点，
      左子树所有值 < node.val < 右子树所有值。
  注意是「**整棵子树**」，不是「只有直接左右孩子」—— 这一点在 LC-0098 会被专门考。

  有了这个不变量，比较一次就能**排除整棵子树**：
      - `val < node.val` ⟹ 它只可能在左子树（右子树全都更大）
      - `val > node.val` ⟹ 只可能在右子树
  于是每一步把搜索空间砍掉一侧 —— 这就是 BST 版的二分查找。

复杂度：**O(h)**，h 是树高。
      - 平衡 BST：h = O(log n)
      - **退化成链**（比如按升序插入建的树）：h = O(n)
      所以**不能无条件说 O(log n)** —— 这是和数组二分最大的区别：
      数组二分**保证** O(log n)，BST 只有在平衡时才有这个保证。

迭代版比递归版更好（空间 O(1) vs O(h)），而且这题的迭代写法非常短，建议默认写迭代。

边界：
  - 空树 → None
  - val 就是根
  - val 不存在 → None
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

##################################################################################################
##### ! Solution 1: 迭代 —— 每次比较砍掉一侧
##### ! 时间复杂度: O(h)（平衡时 O(log n)，退化时 O(n)）   空间复杂度: O(1)
##### ! 适用：BST 搜索的默认写法；比递归省空间
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        cur = root
        while cur and cur.val != val:
            cur = cur.left if val < cur.val else cur.right   # ! 一次比较排除整棵子树
        return cur


##################################################################################################
##### ! Solution 2: 递归（和迭代等价，代码更贴近 BST 的定义）
##### ! 时间复杂度: O(h)   空间复杂度: O(h) 递归栈
##### ! 适用：想强调「BST 的递归结构」时
##################################################################################################


class Solution_2:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root or root.val == val:
            return root
        return self.searchBST(root.left, val) if val < root.val else self.searchBST(root.right, val)


##################################################################################################
##### ! Solution 3: 无视 BST 性质的全树搜索（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：正确性参照 —— 它能跑通但浪费了 BST 的全部优势
##################################################################################################


class Solution_3:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return None
        if root.val == val:
            return root
        return self.searchBST(root.left, val) or self.searchBST(root.right, val)


if __name__ == "__main__":
    import random

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

    root = TreeNode.from_list([4, 2, 7, 1, 3])
    for v in (2, 5, 4, 1):
        a = Solution_1().searchBST(root, v)
        b = Solution_2().searchBST(root, v)
        c = Solution_3().searchBST(root, v)
        got = TreeNode.to_list(a)
        assert got == TreeNode.to_list(b) == TreeNode.to_list(c), v
        print(f"val={v} -> {got}")

    for _ in range(500):                 # ! 随机 BST（含退化成链的情形）对拍
        vals = random.sample(range(0, 30), random.randint(0, 12))
        r = build_bst(vals)
        t = random.randint(-1, 31)
        a, b, c = (Solution_1().searchBST(r, t), Solution_2().searchBST(r, t), Solution_3().searchBST(r, t))
        assert TreeNode.to_list(a) == TreeNode.to_list(b) == TreeNode.to_list(c), (vals, t)
    print("随机对拍 500 组通过 ✓")
