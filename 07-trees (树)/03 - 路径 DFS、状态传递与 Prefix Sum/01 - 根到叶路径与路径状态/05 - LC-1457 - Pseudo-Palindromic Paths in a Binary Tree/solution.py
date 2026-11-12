"""LC-1457 - Pseudo-Palindromic Paths in a Binary Tree

Level 1 · 03 路径 DFS、状态传递与 Prefix Sum → Level 2 · 01 根到叶路径与路径状态

题目在问：节点值是 1..9，数一数有多少条**根到叶**路径上的数字**可以重排成回文**。

### 决定性观察：「能重排成回文」⟺「奇数次出现的数字 ≤ 1 个」

路径上出现次数的奇偶性是全部信息。9 个数字的奇偶性用一个 **9 位 bitmask** 表示：

    mask ^= 1 << val              # ! 出现一次翻转一位
    到叶子时：mask & (mask - 1) == 0   ⟺   mask 最多只有一个 1   ⟺   最多一个数字出现奇数次

`mask & (mask - 1)` 清掉最低位的 1，结果为 0 说明原来至多一个 1 —— 这是位运算里「是不是 2 的幂（或 0）」的标准判据（LC-0231）。

### 和 LC-0112 / LC-0113 的关系

同一个「根到叶 DFS，把路径状态一路传下去」的骨架：
- 0112 传的是 `remaining_sum`
- 0113 传的是 `path` 列表
- 1457 传的是 `mask`（把计数数组压成一个 int）
前序传状态、叶子处判定，就是这一层的全部内容。
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


##################################################################################################
##### ! Solution 1: DFS 传 bitmask，叶子处 mask & (mask-1) == 0
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：面试标准答案。把「奇偶计数」压进一个整数，判定只用一条位运算
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def pseudoPalindromicPaths(self, root: Optional[TreeNode]) -> int:
        def dfs(node, mask):
            if not node:
                return 0
            mask ^= 1 << node.val                         # ! 翻转这一位的奇偶
            if not node.left and not node.right:          # ! 叶子
                return 1 if mask & (mask - 1) == 0 else 0  # ! 至多一个 1
            return dfs(node.left, mask) + dfs(node.right, mask)

        return dfs(root, 0)


##################################################################################################
##### ! Solution 2: 迭代 DFS（显式栈存 (node, mask)）
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：不想递归时；mask 是不可变 int，直接随节点一起入栈，不需要回溯恢复
##################################################################################################


class Solution_2:
    def pseudoPalindromicPaths(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        count, stack = 0, [(root, 0)]
        while stack:
            node, mask = stack.pop()
            mask ^= 1 << node.val
            if not node.left and not node.right:
                count += (mask & (mask - 1)) == 0
            if node.left:
                stack.append((node.left, mask))
            if node.right:
                stack.append((node.right, mask))
        return count


##################################################################################################
##### ! Solution 3: 显式计数数组 + 回溯（bitmask 的「解压」版，真值基线）
##### ! 时间复杂度: O(n · 9)   空间复杂度: O(h + 9)
##### ! 适用：第一次没想到 bitmask 时的写法；叶子处数奇数次的数字个数。必须回溯（进入前 +1，离开后 -1）
##################################################################################################


class Solution_3:
    def pseudoPalindromicPaths(self, root: Optional[TreeNode]) -> int:
        cnt = [0] * 10

        def dfs(node):
            if not node:
                return 0
            cnt[node.val] += 1
            if not node.left and not node.right:
                res = 1 if sum(c & 1 for c in cnt) <= 1 else 0
            else:
                res = dfs(node.left) + dfs(node.right)
            cnt[node.val] -= 1                            # ! 回溯
            return res

        return dfs(root)


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
    cases = [([2, 3, 1, 3, 1, None, 1], 2), ([2, 1, 1, 1, 3, None, None, None, None, None, 1], 1), ([9], 1)]
    for vals, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().pseudoPalindromicPaths(build(vals))
            assert got == want, (cls.__name__, vals, got, want)
    random.seed(1457)
    for _ in range(500):
        n = random.randint(1, 40)
        vals = [random.randint(1, 4) for _ in range(n)]   # ! 值域小，制造大量重复
        for i in range(1, n):
            if random.random() < 0.25:
                vals[i] = None
        root = build(vals)
        outs = [cls().pseudoPalindromicPaths(root) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (vals, outs)
    print("所有测试通过 ✓")
