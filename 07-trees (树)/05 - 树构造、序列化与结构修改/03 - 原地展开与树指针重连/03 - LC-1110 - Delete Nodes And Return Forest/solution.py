"""LC-1110 - Delete Nodes And Return Forest

Level 1 · 05 树构造、序列化与结构修改 → Level 2 · 03 原地展开与树指针重连

题目在问：删掉 `to_delete` 里的节点，剩下的森林里每棵树的根都要收进答案。

### 决定性观察：一个节点成为「新根」的条件

    节点 x 留下来（不被删） 且 （x 是原根 或 x 的父亲被删了）

所以递归时只需要传一个布尔量 **「我的父亲是否还活着」**（或者反过来「我是不是根」）。

### 后序 + 返回值 = 「这个位置以后应该挂谁」

和 LC-0669 一样的骨架：递归函数返回「这个子树修剪后的根」，直接赋回父亲的孩子指针。
被删节点返回 `None`，这样父亲的 `left/right` 自动断开 —— **不需要显式去父节点那里改指针**。

    def dfs(node, parent_alive):
        if not node: return None
        deleted = node.val in to_delete
        if not deleted and not parent_alive: roots.append(node)     # ! 我活着、父亲没了 → 我是新根
        node.left  = dfs(node.left,  not deleted)                    # ! 孩子的「父亲是否活着」= 我是否没被删
        node.right = dfs(node.right, not deleted)
        return None if deleted else node

### 两个细节

- `to_delete` 转成 `set`，否则每个节点 O(len(to_delete)) 查找。
- 处理根：`dfs(root, parent_alive=False)` —— 根「没有父亲」等价于「父亲不在」，正好让根在存活时自动进 roots。
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


##################################################################################################
##### ! Solution 1: 递归返回修剪后的子树根 + 「父亲是否活着」标志
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：面试标准答案；后序保证孩子先被处理完，被删节点返回 None 自动断链
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def delNodes(self, root: Optional[TreeNode], to_delete: List[int]) -> List[TreeNode]:
        kill = set(to_delete)
        roots = []

        def dfs(node, parent_alive):
            if not node:
                return None
            deleted = node.val in kill
            if not deleted and not parent_alive:
                roots.append(node)                         # ! 活着且父亲没了 → 新根
            node.left = dfs(node.left, not deleted)        # ! 孩子视角：父亲活着 ⟺ 我没被删
            node.right = dfs(node.right, not deleted)
            return None if deleted else node

        dfs(root, False)
        return roots


##################################################################################################
##### ! Solution 2: 先收集再断链 —— 把「我是否是根」在前序决定，断链在后序做
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：另一种等价组织：前序时就能判定「我是否新根」（只依赖父亲状态），后序时再把被删孩子置 None。
#####         和 Solution_1 等价，差别只在「先 append 还是后 append」—— 结果顺序不同但集合相同
##################################################################################################


class Solution_2:
    def delNodes(self, root: Optional[TreeNode], to_delete: List[int]) -> List[TreeNode]:
        kill = set(to_delete)
        roots = []

        def dfs(node, is_root):
            if not node:
                return None
            deleted = node.val in kill
            if is_root and not deleted:
                roots.append(node)
            left = dfs(node.left, deleted)                 # ! 我被删 → 孩子成为根候选
            right = dfs(node.right, deleted)
            if deleted:
                return None
            node.left, node.right = left, right
            return node

        dfs(root, True)
        return roots


##################################################################################################
##### ! Solution 3: BFS + 父指针（迭代；用 parent 表显式断链）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：不想递归时。BFS 建 parent 表；遍历每个节点：被删就把父亲对它的指针置 None，并把它活着的孩子记为新根
##################################################################################################


class Solution_3:
    def delNodes(self, root: Optional[TreeNode], to_delete: List[int]) -> List[TreeNode]:
        from collections import deque
        kill = set(to_delete)
        parent = {root: None}
        order, q = [], deque([root])
        while q:
            n = q.popleft(); order.append(n)
            for ch in (n.left, n.right):
                if ch:
                    parent[ch] = n; q.append(ch)
        roots = [] if root.val in kill else [root]
        for n in order:
            if n.val not in kill:
                continue
            p = parent[n]
            if p:                                          # ! 父亲对我的指针断掉
                if p.left is n: p.left = None
                else: p.right = None
            for ch in (n.left, n.right):                   # ! 我活着的孩子成为新根
                if ch and ch.val not in kill:
                    roots.append(ch)
        return roots


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


def serialize(n):
    return None if n is None else (n.val, serialize(n.left), serialize(n.right))


if __name__ == "__main__":
    import random
    for cls in (Solution_1, Solution_2, Solution_3):
        forest = cls().delNodes(build([1, 2, 3, 4, 5, 6, 7]), [3, 5])
        got = sorted(serialize(t) for t in forest)
        assert got == sorted([(1, (2, (4, None, None), None), None), (6, None, None), (7, None, None)]), (cls.__name__, got)
        forest = cls().delNodes(build([1, 2, 4, None, 3]), [3])
        assert sorted(serialize(t) for t in forest) == [(1, (2, None, (3, None, None)), (4, None, None))] if False else True
        got = sorted(serialize(t) for t in cls().delNodes(build([1, 2, 4, None, 3]), [3]))
        assert got == [(1, (2, None, None), (4, None, None))], (cls.__name__, got)
        assert cls().delNodes(build([1]), [1]) == []                         # ! 删掉唯一节点 → 空森林
    random.seed(1110)
    for _ in range(300):
        n = random.randint(1, 25)
        vals = list(range(1, n + 1)); random.shuffle(vals)
        for i in range(1, n):
            if random.random() < 0.25:
                vals[i] = None
        dels = random.sample(range(1, n + 1), random.randint(0, n))
        outs = [sorted(serialize(t) for t in cls().delNodes(build(vals), dels)) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (vals, dels, outs)
    print("所有测试通过 ✓")
