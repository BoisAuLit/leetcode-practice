"""LC-1676 - Lowest Common Ancestor of a Binary Tree IV

Level 1 · 07 LCA、子树关系与树图转换 → Level 2 · 01 Lowest Common Ancestor

题目在问：给**一组**节点 `nodes`（都在树里，互不相同），求它们全体的 LCA。

### 0236 从「两个」推广到「一组」，代码只改一个判断

0236 的递归：「当前节点是 p 或 q 就返回自己；否则左右都非空返回自己，不然返回非空的那边」。
把「是 p 或 q」换成「**在集合里**」，其余一字不改：

    if node in targets: return node

为什么成立？递归的返回值含义是「这个子树里**至少包含一个**目标节点时，它们在这个子树里的 LCA」。
- 当前节点本身是目标 ⟹ 它是它子树里所有目标的祖先 ⟹ 直接返回它（不必再往下，因为答案不可能更深）。
- 左右各有目标 ⟹ 当前节点是分叉点 ⟹ 返回自己。
- 只有一边有 ⟹ 答案在那一边。
这和 0236 的归纳证明完全相同，只是「目标」从 2 个变 k 个。

### 另一条路：两两折叠

`reduce(lca2, nodes)`：LCA 满足结合律 `lca(a, b, c) = lca(lca(a, b), c)`，所以可以用 0236 把 k 个节点逐个折进去。
O(k·n)，比 Solution_1 慢 k 倍，但它展示了「LCA 是一个可结合的二元运算」这个性质 —— 面试里当 follow-up 讲一下即可。
"""
from functools import reduce
from typing import List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


##################################################################################################
##### ! Solution 1: 0236 的递归，把「is p or is q」换成「in 集合」
##### ! 时间复杂度: O(n)（集合查找 O(1)）   空间复杂度: O(h + k)
##### ! 适用：面试标准答案；用 set 存目标，递归一遍树
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def lowestCommonAncestor(self, root: TreeNode, nodes: List[TreeNode]) -> TreeNode:
        targets = set(nodes)                        # ! TreeNode 默认按身份哈希，正好

        def dfs(node):
            if not node or node in targets:         # ! 唯一和 0236 不同的一行
                return node
            l, r = dfs(node.left), dfs(node.right)
            return node if l and r else (l or r)

        return dfs(root)


##################################################################################################
##### ! Solution 2: 两两折叠 reduce(lca2, nodes)
##### ! 时间复杂度: O(k · n)   空间复杂度: O(h)
##### ! 适用：说明 LCA 的结合律；k 小时也完全可用。每次 lca2 都是一遍完整的 0236
##################################################################################################


class Solution_2:
    def lowestCommonAncestor(self, root: TreeNode, nodes: List[TreeNode]) -> TreeNode:
        def lca2(p, q):
            def dfs(node):
                if not node or node is p or node is q:
                    return node
                l, r = dfs(node.left), dfs(node.right)
                return node if l and r else (l or r)
            return dfs(root)

        return reduce(lca2, nodes)                  # ! lca(a,b,c,...) = lca(lca(a,b), c)...


##################################################################################################
##### ! Solution 3: 子树计数 —— 第一个「子树里目标数 == k」的最深节点
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：另一种等价刻画：LCA 是「包含全部 k 个目标的最深节点」。后序返回子树内目标个数，
#####         首次凑满 k 的那个节点就是答案（后序保证先看到更深的）
##################################################################################################


class Solution_3:
    def lowestCommonAncestor(self, root: TreeNode, nodes: List[TreeNode]) -> TreeNode:
        targets, k = set(nodes), len(nodes)
        ans = None

        def count(node) -> int:
            nonlocal ans
            if not node or ans:
                return 0
            c = count(node.left) + count(node.right) + (node in targets)
            if c == k and ans is None:
                ans = node                          # ! 后序：第一个凑满 k 的一定最深
            return c

        count(root)
        return ans


def build_sample():
    nodes = {v: TreeNode(v) for v in (3, 5, 1, 6, 2, 0, 8, 7, 4)}
    nodes[3].left, nodes[3].right = nodes[5], nodes[1]
    nodes[5].left, nodes[5].right = nodes[6], nodes[2]
    nodes[1].left, nodes[1].right = nodes[0], nodes[8]
    nodes[2].left, nodes[2].right = nodes[7], nodes[4]
    return nodes


if __name__ == "__main__":
    import random
    nd = build_sample()
    cases = [([4, 7], 2), ([1], 1), ([7, 6, 2, 4], 5), ([0, 1, 2, 3, 4, 5, 6, 7, 8], 3), ([5, 4], 5)]
    for cls in (Solution_1, Solution_2, Solution_3):
        for ids, want in cases:
            got = cls().lowestCommonAncestor(nd[3], [nd[i] for i in ids])
            assert got is nd[want], (cls.__name__, ids, got.val)
    random.seed(1676)
    allv = list(nd)
    for _ in range(500):
        ids = random.sample(allv, random.randint(1, len(allv)))
        outs = [cls().lowestCommonAncestor(nd[3], [nd[i] for i in ids]) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] is outs[1] is outs[2], (ids, [o.val for o in outs])
    print("所有测试通过 ✓")
