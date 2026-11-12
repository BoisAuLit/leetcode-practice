"""LC-0114 - Flatten Binary Tree to Linked List

Level 1 · 05 树构造、序列化与结构修改 —— **原地（in-place）指针重连**
题目在问：把二叉树按**前序顺序**原地展开成一条「只用 right 指针」的链表，
         所有 left 必须置 None。

决定性观察：
  1. 结果的顺序是**前序**（根 → 左 → 右）。所以链表里根的下一个是原来的左子树的头。
  2. **难点在于「原地」**：当你把 `root.right = root.left` 时，
     原来的右子树就被覆盖了 —— 必须先把它存下来，或者换一个遍历顺序让它先被处理完。
  3. 两个干净的思路：
     - **反向前序**（右 → 左 → 根）：按「根-左-右」的**逆序**访问，
       用一个 `prev` 记住上一个处理过的节点，每次 `node.right = prev; node.left = None; prev = node`。
       因为是逆序，`prev` 永远是「当前节点在最终链表里的下一个」，不会覆盖还没处理的东西。
     - **Morris 式原地穿线**（O(1) 空间）：对每个有左子树的节点，
       找到左子树的**最右节点**（它在前序里正好排在原右子树之前），
       把原右子树挂到它的 right 上，然后把左子树整体搬到 right，left 置 None，继续往下。

为什么反向前序能避免覆盖：
      我们是**从链表尾部往前**构建的。处理节点 X 时，X 之后的所有节点都已经连好并由 `prev` 指着，
      而 X 的左右子树都已经处理完毕，所以直接改 X 的指针不会丢任何东西。

复杂度：
  - 反向前序：O(n) 时间，**O(h) 空间**（递归栈）。
  - Morris 穿线：O(n) 时间（每条边最多走常数次），**O(1) 额外空间**。
    这是本题被追问时的加分答案。

边界：
  - 空树 → 空
  - 只有左子树 / 只有右子树
  - 单节点
  - 完全二叉树
  - 展开后必须所有 left 都是 None（测试里专门校验）
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
##### ! Solution 1: Morris 式原地穿线 —— O(1) 额外空间
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：被追问「能不能 O(1) 空间」时的答案；也是理解「左子树最右节点」这个位置的好例子
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def flatten(self, root: Optional[TreeNode]) -> None:
        cur = root
        while cur:
            if cur.left:
                rightmost = cur.left            # ! 左子树的最右节点，在前序里正好排在原右子树之前
                while rightmost.right:
                    rightmost = rightmost.right
                rightmost.right = cur.right     # ! 把原右子树挂到它后面
                cur.right = cur.left            # ! 左子树整体搬到右边
                cur.left = None                 # ! 题目要求 left 置空
            cur = cur.right


##################################################################################################
##### ! Solution 2: 反向前序（右 → 左 → 根）+ prev 指针
##### ! 时间复杂度: O(n)   空间复杂度: O(h) 递归栈
##### ! 适用：最容易口述的写法；核心是「从链表尾部往前连，就不会覆盖未处理的子树」
##################################################################################################


class Solution_2:
    def __init__(self):
        self.prev = None

    def flatten(self, root: Optional[TreeNode]) -> None:
        self.prev = None

        def dfs(node):
            if not node:
                return
            dfs(node.right)       # ! 先右
            dfs(node.left)        # ! 再左
            node.right = self.prev   # ! 最后处理根：prev 正是它在链表里的下一个
            node.left = None
            self.prev = node

        dfs(root)


##################################################################################################
##### ! Solution 3: 先收集前序序列，再重新串起来（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 直接表达「展开顺序 == 前序」这个定义
##################################################################################################


class Solution_3:
    def flatten(self, root: Optional[TreeNode]) -> None:
        nodes: List[TreeNode] = []

        def pre(node):
            if not node:
                return
            nodes.append(node)
            pre(node.left)
            pre(node.right)

        pre(root)
        for i in range(len(nodes) - 1):
            nodes[i].left = None
            nodes[i].right = nodes[i + 1]
        if nodes:
            nodes[-1].left = nodes[-1].right = None


if __name__ == "__main__":
    import random

    def chain(root):
        """把展开后的结果读成列表，同时校验所有 left 都是 None。"""
        out = []
        cur = root
        while cur:
            assert cur.left is None, "展开后 left 必须全部为 None"
            out.append(cur.val)
            cur = cur.right
        return out

    def preorder(root):
        return [] if not root else [root.val] + preorder(root.left) + preorder(root.right)

    cases = [[1, 2, 5, 3, 4, None, 6], [], [0], [1, 2], [1, None, 2],
             [1, 2, 3, 4, 5, 6, 7]]
    for vals in cases:
        want = preorder(TreeNode.from_list(vals))
        outs = []
        for Sol in (Solution_1, Solution_2, Solution_3):
            t = TreeNode.from_list(vals)
            Sol().flatten(t)
            outs.append(chain(t))
        assert outs[0] == outs[1] == outs[2] == want, (vals, outs, want)
        print(f"{vals} -> {outs[0]}")

    for _ in range(800):
        vals = [random.choice([random.randint(0, 9), None]) for _ in range(random.randint(0, 12))]
        if vals and vals[0] is None:
            vals[0] = 1
        want = preorder(TreeNode.from_list(vals))
        for Sol in (Solution_1, Solution_2, Solution_3):
            t = TreeNode.from_list(vals)
            Sol().flatten(t)
            assert chain(t) == want, (vals, Sol.__name__)
    print("随机对拍 800 组通过 ✓（三种写法都等于前序序列，且 left 全为 None）")
