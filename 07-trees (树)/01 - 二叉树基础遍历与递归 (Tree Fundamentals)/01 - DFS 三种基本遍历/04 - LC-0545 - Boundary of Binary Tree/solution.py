"""LC-0545 - Boundary of Binary Tree

Level 1 · 01 二叉树基础遍历与递归 → Level 2 · 01 DFS 三种基本遍历

题目在问：按**逆时针**输出二叉树的边界：根 → 左边界（不含叶）→ 所有叶子（从左到右）→ 右边界（自底向上，不含叶）。
Meta 高频，难点全在**定义的边角**而不是算法：

### 三段的精确定义（题面是这么写的，一定要照着写）

| 段 | 定义 | 怎么走 |
|---|---|---|
| 左边界 | 从 root.left 出发，**有左走左，没左才走右**，到叶子为止（叶子不算） | 迭代往下 |
| 叶子 | 所有叶节点，**从左到右**（就是前序 / 中序里叶子出现的顺序） | 任意 DFS |
| 右边界 | 从 root.right 出发，**有右走右，没右才走左**，到叶子为止（叶子不算）；**倒序**输出 | 迭代往下再 reverse |

### 四个坑

1. 根单独输出一次；**根若是叶子（单节点树），只输出一次**，不能在「叶子」段再输出。
2. 左边界 / 右边界**不包含叶子** —— 叶子交给第二段，否则重复。
3. 根只有右子树时，**没有左边界**（不要把右子树的左侧当左边界）；对称地，只有左子树时没有右边界。
4. 右边界要倒序。

把这四条写进代码的注释里，就是面试里能拿满分的方式 —— 这题考的是「读题 + 不漏不重」，不是算法。
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


##################################################################################################
##### ! Solution 1: 三段分别求，再拼接（最清晰、最贴题面）
##### ! 时间复杂度: O(n)   空间复杂度: O(h)（递归栈）+ O(n) 输出
##### ! 适用：面试标准答案。三个小函数一一对应题面的三条定义，坑都在注释里标出来
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def boundaryOfBinaryTree(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        def is_leaf(n): return not n.left and not n.right

        def left_boundary(n) -> List[int]:
            out = []
            while n and not is_leaf(n):              # ! 叶子不进边界，交给 leaves()
                out.append(n.val)
                n = n.left if n.left else n.right     # ! 有左走左，没左才走右
            return out

        def right_boundary(n) -> List[int]:
            out = []
            while n and not is_leaf(n):
                out.append(n.val)
                n = n.right if n.right else n.left    # ! 有右走右，没右才走左
            return out[::-1]                          # ! 自底向上

        def leaves(n, out):
            if not n:
                return
            if is_leaf(n):
                out.append(n.val); return
            leaves(n.left, out); leaves(n.right, out)   # ! 前序中叶子出现的顺序就是从左到右

        if is_leaf(root):
            return [root.val]                         # ! 单节点：根就是叶，只输出一次
        lv = []
        leaves(root, lv)
        return [root.val] + left_boundary(root.left) + lv + right_boundary(root.right)


##################################################################################################
##### ! Solution 2: 一次前序 DFS，用「是否在左边界 / 右边界上」两个标志同时收集三段
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：想只遍历一遍时。标志的传递规则：
#####         左孩子继承「在左边界」当且仅当父在左边界；右孩子在没有左孩子时也可继承左边界（没左走右）；对称处理右边界。
#####         比 Solution_1 难讲清楚，面试里先写 Solution_1，被问「能不能一遍」再说这个
##################################################################################################


class Solution_2:
    def boundaryOfBinaryTree(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        left, leaves, right = [], [], []

        def dfs(n, on_left, on_right):
            if not n:
                return
            if not n.left and not n.right:
                leaves.append(n.val); return
            if on_left:
                left.append(n.val)
            elif on_right:
                right.append(n.val)
            # ! 左孩子：在左边界 ⟺ 父在左边界；右孩子在父没有左孩子时接管左边界
            dfs(n.left, on_left, on_right and not n.right)
            dfs(n.right, on_left and not n.left, on_right)

        if not root.left and not root.right:
            return [root.val]
        dfs(root.left, True, False)
        dfs(root.right, False, True)
        return [root.val] + left + leaves + right[::-1]


##################################################################################################
##### ! Solution 3: 按定义的暴力（真值基线）—— 用集合做去重，顺序靠显式拼接
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：只用来对拍。把「节点身份」而不是值放进列表，最后再取值，避免值重复时误判
##################################################################################################


class Solution_3:
    def boundaryOfBinaryTree(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        seq = [root]
        n = root.left
        while n and (n.left or n.right):
            seq.append(n); n = n.left or n.right
        stack, lv = [root], []
        while stack:                                  # ! 迭代前序收叶子
            x = stack.pop()
            if not x.left and not x.right:
                lv.append(x)
            else:
                if x.right: stack.append(x.right)
                if x.left: stack.append(x.left)
        rb = []
        n = root.right
        while n and (n.left or n.right):
            rb.append(n); n = n.right or n.left
        seen, out = set(), []
        for node in seq + lv + rb[::-1]:
            if id(node) not in seen:                  # ! 单节点树里根既是根又是叶，靠这里去重
                seen.add(id(node)); out.append(node.val)
        return out


def build(vals):
    from collections import deque
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i]); q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i]); q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    import random
    cases = [
        ([1, None, 2, 3, 4], [1, 3, 4, 2]),                      # ! 根没左子树 → 没有左边界
        ([1, 2, 3, 4, 5, 6, None, None, None, 7, 8, 9, 10], [1, 2, 4, 7, 8, 9, 10, 6, 3]),
        ([1], [1]),                                               # ! 单节点
        ([1, 2], [1, 2]),                                         # ! 根 + 一个叶子
        ([1, 2, 3], [1, 2, 3]),
    ]
    for vals, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().boundaryOfBinaryTree(build(vals))
            assert got == want, (cls.__name__, vals, got, want)
    random.seed(545)
    for _ in range(500):
        n = random.randint(1, 30)
        vals = [random.randint(0, 9) for _ in range(n)]
        for i in range(1, n):
            if random.random() < 0.3:
                vals[i] = None
        root = build(vals)
        outs = [cls().boundaryOfBinaryTree(root) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (vals, outs)
    print("所有测试通过 ✓")
