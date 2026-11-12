"""LC-0337 - House Robber III

Level 1 · 02 后序信息汇总与 Tree DP —— **多状态返回值**的标准范例
题目在问：二叉树上每个节点有一笔钱，**不能同时抢相邻（父子）的两个节点**，求最大收益。

决定性观察（本题要回答的核心问题是「dfs 应该返回什么」）：
  1. 只返回「这棵子树的最大收益」是**不够的**：
     父节点需要知道「孩子被抢了没有」才能决定自己能不能抢。
     单个数字丢掉了这个信息。
  2. 所以 dfs 返回**两个状态**：
        `rob`  = 抢了当前节点时，这棵子树的最大收益
        `skip` = 不抢当前节点时，这棵子树的最大收益
  3. 转移：
        rob  = node.val + left.skip + right.skip   （抢了自己，孩子必须跳过）
        skip = max(left.rob, left.skip) + max(right.rob, right.skip)
               （不抢自己，孩子**各自**随意取最优）
     答案 = `max(rob, skip)`。

**`skip` 用 max 而不是直接取 `rob`**：不抢自己时孩子**可抢可不抢**，要取两者较优。
这一步写错是最常见的 bug。

为什么必须是 Postorder（自底向上）：
      父节点的两个状态都依赖孩子的两个状态，所以**必须先算完孩子**。
      这正是 Bottom-up DFS 的定义。

与 LC-0198 / LC-0213（数组版打家劫舍）的关系：
      数组版是「线性 DP，两个状态沿着下标推进」；
      树版是「树形 DP，两个状态沿着树边向上汇总」。
      **状态定义完全一样，只是递推的拓扑结构从链变成了树。**
      想不清楚的时候，把树退化成一条链（每个节点只有左孩子）对照看。

复杂度：O(n) 时间（每个节点访问一次），O(h) 空间（递归栈，最坏 O(n)）。

边界：
  - 空树 → 0
  - 单节点 → 该节点的值
  - 一条链 [1,2,None,3] → 退化成数组版打家劫舍
  - 全是大额在叶子上 → skip 根、抢所有叶子
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
##### ! Solution 1: 树形 DP —— dfs 返回 (rob, skip) 两个状态
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：所有「选了某个节点就不能选相邻节点」的树上最优化问题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            """返回 (抢这个节点的最优解, 不抢这个节点的最优解)。"""
            if not node:
                return (0, 0)
            lr, ls = dfs(node.left)
            rr, rs = dfs(node.right)
            rob_here = node.val + ls + rs           # ! 抢自己 → 两个孩子都必须 skip
            skip_here = max(lr, ls) + max(rr, rs)   # ! 不抢自己 → 孩子各自取最优（注意是 max）
            return (rob_here, skip_here)

        return max(dfs(root))


##################################################################################################
##### ! Solution 2: 朴素递归 + 记忆化（把「孩子抢没抢」编码进 memo 的 key）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：先想到这版再优化成 Solution_1 也很自然；但它多了一个字典的常数开销
##################################################################################################


class Solution_2:
    def rob(self, root: Optional[TreeNode]) -> int:
        memo = {}

        def dfs(node, can_rob: bool) -> int:
            if not node:
                return 0
            key = (id(node), can_rob)
            if key in memo:
                return memo[key]
            best = dfs(node.left, True) + dfs(node.right, True)      # ! 不抢自己
            if can_rob:                                              # ! 抢自己
                best = max(best, node.val + dfs(node.left, False) + dfs(node.right, False))
            memo[key] = best
            return best

        return dfs(root, True)


##################################################################################################
##### ! Solution 3: 暴力枚举所有合法选法（基准答案，用来对拍；只适合很小的树）
##### ! 时间复杂度: 指数级   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 直接按题面「不能选相邻」的定义穷举
##################################################################################################


class Solution_3:
    def rob(self, root: Optional[TreeNode]) -> int:
        nodes, parent = [], {}

        def collect(node, par):
            if not node:
                return
            nodes.append(node)
            parent[id(node)] = par
            collect(node.left, node)
            collect(node.right, node)

        collect(root, None)
        n = len(nodes)
        best = 0
        for mask in range(1 << n):
            chosen = {id(nodes[i]) for i in range(n) if mask >> i & 1}
            ok = all(parent[nid] is None or id(parent[nid]) not in chosen for nid in chosen)
            if ok:
                best = max(best, sum(nodes[i].val for i in range(n) if mask >> i & 1))
        return best


if __name__ == "__main__":
    import random

    cases = [[3, 2, 3, None, 3, None, 1], [3, 4, 5, 1, 3, None, 1], [], [5],
             [1, 2, None, 3], [4, 1, None, 2, None, 3]]
    for vals in cases:
        a = Solution_1().rob(TreeNode.from_list(vals))
        b = Solution_2().rob(TreeNode.from_list(vals))
        c = Solution_3().rob(TreeNode.from_list(vals))
        assert a == b == c, (vals, a, b, c)
        print(f"{vals} -> {a}")

    for _ in range(300):                 # ! 随机小树三方对拍
        vals = [random.choice([random.randint(0, 9), None]) for _ in range(random.randint(0, 10))]
        if vals and vals[0] is None:
            vals[0] = 1
        a = Solution_1().rob(TreeNode.from_list(vals))
        b = Solution_2().rob(TreeNode.from_list(vals))
        c = Solution_3().rob(TreeNode.from_list(vals))
        assert a == b == c, (vals, a, b, c)
    print("随机对拍 300 组通过 ✓")
