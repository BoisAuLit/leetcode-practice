"""LC-1644 - Lowest Common Ancestor of a Binary Tree II

Level 1 · 07 LCA、子树关系与树图转换 → Level 2 · 01 Lowest Common Ancestor

题目在问：和 LC-0236 一样求 LCA，**但 p 或 q 可能不在树里**，不在就返回 `None`。

### 为什么 0236 的代码直接搬过来是错的

0236 的递归有一个「偷懒」：找到 p 或 q 就立刻返回，不再往下看。这依赖题目保证「p、q 都在树里」——
如果 q 是 p 的后代，0236 返回 p 是对的（p 是 LCA）；但本题里 q 可能**根本不存在**，这时正确答案是 `None`，
0236 却照样返回 p。

    0236 的隐含假设：「碰到 p，就不用再确认 q 在不在」
    1644 把这个假设拿掉了 ⟹ 必须把整棵树走完，数清楚到底见到了几个

### 两条修法

1. **遍历全树 + 计数**（一遍）：递归照 0236 写，但**不提前返回**（先递归两个孩子，再判断当前节点），
   并用一个计数器记录见到了 p、q 中的几个。结束时 `count == 2` 才返回 LCA，否则 `None`。
2. **先用 0236 求 LCA，再验证**（两遍）：求出候选 `lca` 后，若 `lca is p`，在 p 的子树里找 q；若 `lca is q`，找 p；
   否则两者都在（因为 0236 在 p、q 都不是对方祖先时只有两者都存在才会返回非空非 p/q 的节点）。
   这条思路把「正确性」拆成「0236 + 一次存在性检查」，面试里更容易讲清楚。
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


##################################################################################################
##### ! Solution 1: 后序遍历全树 + 计数（不提前返回）
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：面试标准答案。和 0236 的区别只有两处：① 先递归再判断自己（保证走完全树）② 记 found 计数。
#####         把这两处差别说出来，就是本题的全部考点
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
        found = 0

        def dfs(node):
            nonlocal found
            if not node:
                return None
            left = dfs(node.left)                  # ! 先把两边都走完 —— 0236 在这里会提前 return
            right = dfs(node.right)
            if node is p or node is q:
                found += 1                         # ! 记住见过几个
                return node
            return node if left and right else (left or right)

        ans = dfs(root)
        return ans if found == 2 else None         # ! 只见到一个或没见到 → 不存在 LCA


##################################################################################################
##### ! Solution 2: 先按 0236 求候选 LCA，再做一次存在性检查
##### ! 时间复杂度: O(n)（两遍）   空间复杂度: O(h)
##### ! 适用：把问题拆成「已会的 0236」+「子树里找节点」。候选是 p 时 q 必须在 p 的子树里，反之亦然；
#####         候选是别的节点时 p、q 一定都存在（0236 的返回值性质）
##################################################################################################


class Solution_2:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
        def lca236(node):
            if not node or node is p or node is q:
                return node
            l, r = lca236(node.left), lca236(node.right)
            return node if l and r else (l or r)

        def contains(node, target):
            if not node:
                return False
            return node is target or contains(node.left, target) or contains(node.right, target)

        cand = lca236(root)
        if cand is None:
            return None
        if cand is p:
            return p if contains(p, q) else None   # ! 候选是 p：q 必须在 p 的子树里
        if cand is q:
            return q if contains(q, p) else None
        return cand                                # ! 候选是第三者：说明左右各找到一个，p、q 都在


##################################################################################################
##### ! Solution 3: 父指针 + 祖先集合（迭代写法，顺带兼容「p/q 不存在」）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：想避开递归、或者树太深时。BFS 建 parent 表时若没见到 p 或 q 直接返回 None；
#####         然后从 p 往上走把祖先放进集合，再从 q 往上走，第一个在集合里的就是 LCA（和 LC-1650 同一招）
##################################################################################################


class Solution_3:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
        from collections import deque
        parent = {root: None}
        dq = deque([root])
        while dq:
            node = dq.popleft()
            for ch in (node.left, node.right):
                if ch:
                    parent[ch] = node
                    dq.append(ch)
        if p not in parent or q not in parent:   # ! 任一不在树里
            return None
        anc = set()
        while p:
            anc.add(p); p = parent[p]
        while q not in anc:
            q = parent[q]
        return q


def build_sample():
    #           3
    #        /     \
    #       5       1
    #      / \     / \
    #     6   2   0   8
    #        / \
    #       7   4
    nodes = {v: TreeNode(v) for v in (3, 5, 1, 6, 2, 0, 8, 7, 4)}
    nodes[3].left, nodes[3].right = nodes[5], nodes[1]
    nodes[5].left, nodes[5].right = nodes[6], nodes[2]
    nodes[1].left, nodes[1].right = nodes[0], nodes[8]
    nodes[2].left, nodes[2].right = nodes[7], nodes[4]
    return nodes


if __name__ == "__main__":
    nodes = build_sample()
    outside = TreeNode(10)                         # ! 不在树里的节点
    cases = [((5, 1), 3), ((5, 4), 5), ((7, 8), 3), ((6, 7), 5)]        # ! 题目保证 p != q
    for cls in (Solution_1, Solution_2, Solution_3):
        for (a, b), want in cases:
            got = cls().lowestCommonAncestor(nodes[3], nodes[a], nodes[b])
            assert got is nodes[want], (cls.__name__, a, b, got and got.val)
        # ! 关键用例：q 不存在，而 p 在树里 —— 0236 会错误地返回 p，本题必须返回 None
        assert cls().lowestCommonAncestor(nodes[3], nodes[5], outside) is None, cls.__name__
        assert cls().lowestCommonAncestor(nodes[3], outside, nodes[4]) is None, cls.__name__
        assert cls().lowestCommonAncestor(nodes[3], outside, TreeNode(11)) is None, cls.__name__
    print("所有测试通过 ✓")
