"""LC-0173 - Binary Search Tree Iterator

Level 1 · 04 BST 有序性质与操作 —— **Lazy（惰性）中序遍历**
题目在问：实现一个 BST 迭代器，`next()` 按**升序**返回下一个值，`hasNext()` 判断还有没有。
         要求 `next` / `hasNext` 平均 O(1)，空间 O(h)。

**本题的全部教学价值在于「不要一次性遍历完」**：
  把整棵树中序遍历进一个数组，然后用下标走 —— 功能上完全正确，
  但那是 O(n) 空间，而且**丢掉了这道设计题想考的东西**。
  题目明确给了 O(h) 空间的要求，就是要你写惰性版本。

决定性观察：
  1. 中序遍历 = 「一路向左走到底，访问，然后转向右子树，重复」。
  2. 把「一路向左」这条**路径**存进栈里。
     **栈顶永远是下一个该返回的节点** —— 因为它是当前未访问部分中最左的。
  3. `next()`：弹出栈顶 node，返回它的值；
     然后把 `node.right` 的「一路向左」路径压进栈（为下一次做准备）。
  4. `hasNext()`：栈非空即可。

```python
def _push_left(self, node):
    while node:
        self.stack.append(node)
        node = node.left
```

复杂度（这里要说准）：
  - 空间 **O(h)** —— 栈里只存一条从某节点到最左的路径。
  - `next()` 单次最坏 **O(h)**（刚好要压一条很长的左链），
    但 n 次调用总共只会把每个节点压入/弹出各一次 ⟹ 总 O(n) ⟹ **摊还 O(1)**。
    **不能不加说明地说单次 O(1)。** 这个措辞和 LC-0901 Online Stock Span、
    LC-0232 两栈队列是同一类摊还分析。

和 LC-0230 Kth Smallest 的关系：
      230 可以直接复用这个迭代器 —— 调 k 次 `next()` 即可，而且**能提前退出**，
      不必遍历整棵树。这正是惰性设计的实际好处。

边界：
  - 空树 → `hasNext()` 直接 False
  - 单节点
  - 退化成左链 / 右链的 BST
  - 连续调用 `hasNext()` 多次不应该改变状态
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
##### ! Solution 1: 惰性中序 —— 栈里只保存「一路向左」的路径
##### ! 时间复杂度: next/hasNext 摊还 O(1)（单次最坏 O(h)）   空间复杂度: O(h)
##### ! 适用：所有「按中序逐个产出、且希望能随时停下」的 BST 场景
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class BSTIterator_1:
    def __init__(self, root: Optional[TreeNode]):
        self.stack: List[TreeNode] = []
        self._push_left(root)

    def _push_left(self, node) -> None:
        while node:                       # ! 一路向左，路径全压进栈
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        node = self.stack.pop()           # ! 栈顶就是当前最小的未访问节点
        self._push_left(node.right)       # ! 它的右子树的最左链，是下一批候选
        return node.val

    def hasNext(self) -> bool:
        return len(self.stack) > 0


##################################################################################################
##### ! Solution 2: 预先中序遍历进数组（能过，但不符合题目的 O(h) 空间意图）
##### ! 时间复杂度: 构造 O(n)，next/hasNext O(1)   空间复杂度: **O(n)**
##### ! 适用：仅作对照 —— 面试写这个会被追问「能不能 O(h) 空间」
##################################################################################################


class BSTIterator_2:
    def __init__(self, root: Optional[TreeNode]):
        self.vals: List[int] = []
        self.i = 0

        def inorder(node):
            if not node:
                return
            inorder(node.left)
            self.vals.append(node.val)
            inorder(node.right)

        inorder(root)

    def next(self) -> int:
        v = self.vals[self.i]
        self.i += 1
        return v

    def hasNext(self) -> bool:
        return self.i < len(self.vals)


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

    root = TreeNode.from_list([7, 3, 15, None, None, 9, 20])
    it = BSTIterator_1(root)
    out = []
    while it.hasNext():
        out.append(it.next())
    print("中序输出:", out)
    assert out == [3, 7, 9, 15, 20]

    it = BSTIterator_1(None)
    assert it.hasNext() is False
    print("空树 hasNext ->", it.hasNext())

    for _ in range(500):                 # ! 随机 BST：惰性版和数组版必须产出完全相同的序列
        vals = random.sample(range(0, 40), random.randint(0, 14))
        r1, r2 = build_bst(vals), build_bst(vals)
        a, b = BSTIterator_1(r1), BSTIterator_2(r2)
        o1, o2 = [], []
        while a.hasNext():
            assert a.hasNext() and a.hasNext()      # ! 多次调用 hasNext 不应改变状态
            o1.append(a.next())
        while b.hasNext():
            o2.append(b.next())
        assert o1 == o2 == sorted(vals), (vals, o1, o2)
    print("随机对拍 500 组通过 ✓（惰性中序 == 排序结果）")
